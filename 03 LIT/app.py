from groq import Groq
import streamlit as st

from config import OPEN_AI_KEY as api_key
print("OPEN_AI_KEY:", len(api_key))

client = Groq(api_key=api_key)
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b", temperature=1,
    max_completion_tokens=2048, top_p=1,
    reasoning_effort="medium", stream=True,
    stop=None, messages=[{"role": "developer", "content": "Hello world"}]
)

st.set_page_config(page_title="Streamlit Chat", page_icon="🤖")
st.title(":blue[Chat]:yellow[Bot]")

if "model" not in st.session_state:
    st.session_state.model = "openai/gpt-oss-120b"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a HR executive for Amazon. You are interviewing a user named Olivia for the position of Data Scientist at a Junior level.\n\nThe interviewee has no experience.\n\nThe interviewee possesses the following skills: Python, Machine Learning and Data Analysis.\n\nUse these details to create two of your questions:\n- Can you share an example of a data-related problem you encountered and how you approached solving it?\n- How do you prioritize tasks when working on multiple data projects with tight deadlines?\n\nAsk each question individually, creating a conversational flow rather than presenting all the questions simultaneously."
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Your answer."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("ai"):
        stream = client.chat.completions.create(
            model=st.session_state.model, temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )
        response = st.write_stream(
            chunk.choices[0].delta.content
            for chunk in stream
            if chunk.choices[0].delta.content
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
