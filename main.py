import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

st.title("Sarthi")
st.caption("Your personal AI assistant")

st.subheader("What can Sarthi do?")

st.markdown("""
    - Answer questions on various topics
    - Arrange calendar events and meetings
    - Read, summarize, and reply to emails
    - Manage tasks and to-do lists
    - Take quick notes
    - Track expenses
""")

st.subheader("Chat with Sarthi")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("Ask Sarthi anything...")

if user_message:
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Sarthi is thinking..."):
            try:
                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json={"message": user_message},
                    timeout=30,
                )
                response.raise_for_status()

                data = response.json()
                ai_response = data[0]["output"]

            except requests.RequestException:
                ai_response = "Sorry, I couldn't connect to Sarthi right now."

            except (ValueError, KeyError, IndexError):
                ai_response = "Sarthi returned an unexpected response."

        st.markdown(ai_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })