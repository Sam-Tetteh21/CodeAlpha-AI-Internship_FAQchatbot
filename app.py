"""
CodeAlpha - Chatbot for FAQs
Task 2: AI Internship

A chat-style web app that answers student questions by matching them
against a set of pre-written FAQs using TF-IDF + cosine similarity
(see chatbot_engine.py for how the matching works).
"""

import streamlit as st

from chatbot_engine import FAQChatbot
from faqs import FAQS

st.set_page_config(page_title="CodeAlpha FAQ Chatbot", page_icon="🎓")
st.title("🎓 University Student Services FAQ Chatbot")
st.caption("CodeAlpha AI Internship - Task 2")

# ---------------------------------------------------------------------
# Build the chatbot once and cache it, so it doesn't reprocess the
# FAQs on every single interaction (Streamlit re-runs the whole script
# on every click/keystroke, so caching avoids repeated work).
# ---------------------------------------------------------------------
@st.cache_resource
def load_chatbot():
    return FAQChatbot(FAQS)


chatbot = load_chatbot()

with st.expander("💡 Example questions you can ask"):
    st.markdown(
        "- How do I register for courses?\n"
        "- I lost my ID card, what do I do?\n"
        "- When are exams?\n"
        "- How do I pay my fees?\n"
        "- How do I get a transcript?"
    )

# ---------------------------------------------------------------------
# Keep chat history across reruns using Streamlit's session_state,
# which persists data for one browser session.
# ---------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I'm the Student Services FAQ bot. Ask me about registration, exams, fees, IDs, and more.",
        }
    ]

# Redraw the full conversation history each time.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------------------------
# Handle new user input
# ---------------------------------------------------------------------
user_input = st.chat_input("Type your question here...")

if user_input:
    # Show and store the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get the chatbot's answer
    answer, matched_question, score = chatbot.get_response(user_input)

    # Show and store the assistant's reply
    with st.chat_message("assistant"):
        st.markdown(answer)
        if matched_question:
            st.caption(f"Matched FAQ: \u201c{matched_question}\u201d (confidence: {score:.0%})")

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
st.caption("Built with Python, Streamlit, NLTK, and scikit-learn (TF-IDF + cosine similarity).")
