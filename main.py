import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv

import ui

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
REQUEST_TIMEOUT = 60  # agent workflows with tool calls can take a while

st.set_page_config(page_title="Sarthi", page_icon="🧭", layout="centered")
ui.inject_css()


def queue_prompt(text: str) -> None:
    """Callback for suggestion buttons: runs before the rerun starts."""
    st.session_state.pending_prompt = text


def ask_sarthi(message: str) -> tuple[str, bool]:
    """Send a message to the n8n webhook. Returns (text, ok)."""
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": message},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        item = data[0] if isinstance(data, list) else data
        return item["output"], True

    except requests.Timeout:
        return "Sarthi took too long to respond. Try again, or split the request into smaller steps.", False
    except requests.RequestException:
        return "Couldn't reach Sarthi. Check that the n8n workflow is active and the webhook URL is correct.", False
    except (ValueError, KeyError, IndexError, TypeError):
        return "Sarthi sent back something unexpected. Check the workflow's `output` field in n8n.", False


def stream_words(text: str):
    """Reveal the reply word by word (n8n returns it all at once)."""
    words = text.split(" ")
    delay = min(0.015, 2.5 / max(len(words), 1))
    for word in words:
        yield word + " "
        time.sleep(delay)


st.session_state.setdefault("messages", [])

if not N8N_WEBHOOK_URL:
    st.error("`N8N_WEBHOOK_URL` is not set. Add it to your `.env` file and restart the app.")
    st.stop()

ui.render_header()

prompt = st.chat_input("Ask Sarthi anything...") or st.session_state.pop("pending_prompt", None)

for message in st.session_state.messages:
    ui.render_message(message)

if not st.session_state.messages and not prompt:
    ui.lock_scroll()
    ui.render_welcome(on_pick=queue_prompt)

if prompt:
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    ui.render_message(user_msg)

    with ui.bubble("assistant"):
        with st.spinner("Sarthi is thinking..."):
            reply, ok = ask_sarthi(prompt)
        if ok:
            st.write_stream(stream_words(reply))
        else:
            st.error(reply, icon=":material/error:")

    st.session_state.messages.append({"role": "assistant", "content": reply, "error": not ok})