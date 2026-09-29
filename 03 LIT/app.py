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
st.subheader("Personal Information", divider="red")
name = st.text_input(label="Name", placeholder="Enter your name")
experience = st.text_area(label="Experience", placeholder="Describe your experience")
skills = st.text_area(label="Skills", placeholder="List your skills")
data = {"name": name, "exp": experience, "skills": skills}
st.write(data)
st.write(f"**Your name**: {name}")
st.write(f"**Your Experience**: {experience}")
st.write(f"**Your Skills**: {skills}")

st.subheader("Company and Position", divider="orange")
col1, col2, col3 = st.columns(3)
with col1:
    company = st.selectbox("Choose Company", ("Amazon", "Meta", "Udemy", "Spotify", "Nestle", "X"))
with col2:
    level = st.radio("Choose Level", options=["Junior", "Mid-level", "Senior"], key="visibility")
with col3:
    position = st.selectbox("Choose position", ("Django Engineer", "Data Engineer", "ML Engineer", "AI Scientist", "Data Scientist", "Python Programmer"))


if "model" not in st.session_state:
    st.session_state.model = "openai/gpt-oss-120b"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are a HR executive. You are interviewing a user named {name} for the position of {position} at a {level} level for the {company} company.\n\nThe interviewee has the following experience: {experience}.\n\nThe interviewee possesses the following skills: {skills}\n\nAsk each question individually, creating a conversational flow rather than presenting all the questions simultaneously."
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system1":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Interviewer Side
st.subheader("Interviewer Side", divider="rainbow")

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
