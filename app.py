# app.py
import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="GenAI Ops Assistant",
    layout="wide"
)

st.title("GenAI Ops Assistant")
st.caption("Ask questions about logs, incidents, and services")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**User:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")

# Chat input
user_input = st.chat_input("Ask about logs, incidents, or services")

if user_input:
    # Store user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Analyzing..."):
        response = run_agent(user_input)

    # Store assistant message
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# Optional reset
if st.button("Reset conversation"):
    st.session_state.chat_history = []
    st.rerun()