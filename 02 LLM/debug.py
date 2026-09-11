# Since I can't debug in jupyter, let's do it here.

from collections.abc import Sequence

from langchain_core.messages import (
    HumanMessage,
    BaseMessage,
    AIMessage,
    RemoveMessage,
    SystemMessage,
)
from langgraph.graph import START, END, StateGraph, add_messages, MessagesState
from langchain_openai.chat_models import ChatOpenAI
from typing_extensions import TypedDict, Annotated

from config import OPEN_AI_KEY as API_KEY

chat = ChatOpenAI(model="gpt-5.6-luna", seed=365, temperature=0, api_key=API_KEY)


def chatbot(_state: MessagesState) -> MessagesState:
    print("\n----------------> Entering ChatBot:")
    _response = chat.invoke(_state.get("messages"))
    _response.pretty_print()
    return MessagesState(messages=[_response])


def ask_question(_state: MessagesState) -> MessagesState:
    print("\n----------------> Entering Ask Question Node:")
    print("What is your question?")
    question = input()
    print("\nQuestion: ", question)
    return MessagesState(messages=[HumanMessage(question)])


def ask_another_question(_state: MessagesState) -> MessagesState:
    print("\n----------------> Asking Another Question:")
    question = "Would you like to ask one more question (yes/no)?"
    print(question)
    _result = "yes" if input().lower().startswith("y") else "no"
    print("\nHi: ", _result)
    return MessagesState(messages=[AIMessage(question), HumanMessage(_result)])


def trim_messages(_state: MessagesState) -> MessagesState:
    print("\n----------------> Trimming Messages:")
    removed_msg = [RemoveMessage(id=msg.id) for msg in _state["messages"][:-5]]
    return MessagesState(messages=removed_msg)


# Define the routing function
def routing_function(_state: MessagesState) -> bool:
    print("\n----------------> Entering Routing Node:")
    if _state["messages"][-1].content == "yes":
        return True
    else:
        print("Bye!")
        return False


class CustomState(MessagesState):
    summary: str


# Should make others custom state too but since it's inheriting from message
# state, let's leave it and see
def chatbot(_state: CustomState) -> CustomState:
    print("\n----------------> Entering ChatBot:")
    _msg = f"""Here's a quick summary of what's been discussed so far: 
    {_state.get("summary", "")}
    Keep this in mind as you answer the next question.
    """
    _response = chat.invoke([SystemMessage(_msg)] + _state.get("messages"))
    _response.pretty_print()
    return CustomState(messages=[_response])


def summarize_and_delete_messages(_state: CustomState) -> CustomState:
    print("\n----------------> Summarizing & Deleting Messages:")

    new_convo = ""
    for _msg in _state["messages"]:
        new_convo += f"{_msg.type.capitalize()}: {_msg.content.capitalize()}\n\n"

    instructions = f"""Update the ongoing summary by incorporating the new lines of conversations below.
    Build upon the previous summary rather than repeating it so that the result reflects the most recent context & developments.
    Previous Summary: {_state.get("summary", "")}
    New Conversation: {new_convo}
    """

    summary = chat.invoke([HumanMessage(instructions)])
    remove_messages = [RemoveMessage(id=_msg.id) for _msg in _state.get("messages")]
    return CustomState(messages=remove_messages, summary=summary.content)


graph = StateGraph(CustomState)

graph.add_node("ask_question", ask_question)
graph.add_node("chatbot", chatbot)
graph.add_node("ask_another_question", ask_another_question)
graph.add_node("summarize_and_delete_messages", summarize_and_delete_messages)

graph.add_edge(START, "ask_question")
graph.add_edge("ask_question", "chatbot")
graph.add_edge("chatbot", "ask_another_question")
graph.add_conditional_edges(
    "ask_another_question",
    routing_function,
    {True: "summarize_and_delete_messages", False: "__end__"},
)
graph.add_edge("summarize_and_delete_messages", "ask_question")

graph_compiled = graph.compile()

response = graph_compiled.invoke(CustomState(messages=[]))
