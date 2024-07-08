import streamlit as st
from dataclasses import dataclass

st.title("Echo Bot")


@dataclass
class Message:
    actor: str
    payload: str


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

USER = "user"
ASSISTANT = "Bob The AI"

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message(USER):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": USER, "content": prompt})

    # Create and display assistant's response
    assistant_response = f"You wrote {prompt}"
    st.session_state.messages.append({"role": ASSISTANT, "content": assistant_response})
    with st.chat_message(ASSISTANT):
        st.write(assistant_response)


    #streamlit run C:/Users/leahw/PycharmProjects/Int-to-Artificial-Intelligence-Final-Project/Main.py