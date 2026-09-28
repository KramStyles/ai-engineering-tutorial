import streamlit as st

# st.title("Hello, Streamlitttt!!!")
# st.title("_This_ is :blue[a title]")
# st.title("$E = mc^2$")
# st.header("This is a :red[header]")
# st.subheader("This is a :yellow[sub header]")
# st.text("This is a plain text")
# st.markdown("""
# # This is a header\n **This is a bold text** \n - This is a list item
# """)
# st.write("This is another plain text using write()")
# data = {"Name": "Olivia", "Age": 26, "Occupation": "Newscaster"}
# st.write(data)

# with st.chat_message("user"):
#     st.write("Hello, there!")

# prompt = st.chat_input("Type your message", max_chars=50)
# if prompt:
#     st.write(f"User: {prompt}")

# with st.chat_message("human"): st.write("Hi there")
# with st.chat_message("ai"): st.write("Hi there")
# with st.chat_message("Z"): st.write("Hi there")
    
if "show_second_button" not in st.session_state:
    st.session_state.show_second_button = False

if st.button("First Button"):
    st.session_state.show_second_button = True

if st.session_state.show_second_button:
    st.write("Revealed")

    if st.button("Second Button"):
        with st.chat_message("human"):
            st.write("Hi there")