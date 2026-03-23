import streamlit as st
from openai import OpenAI
import os

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.chat-container {
    max-width: 700px;
    margin: auto;
}
.user-msg {
    background-color: #DCF8C6;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    text-align: right;
}
.bot-msg {
    background-color: #F1F0F0;
    padding: 10px 15px;
    border-radius: 15px;
    margin: 5px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("🤖 AI Chatbot")
st.caption("Smart • Fast • Interactive")
st.markdown("---")

# -------------------- OPENAI CLIENT --------------------
# client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant. Reply clearly and simply."
        }
    ]

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Settings")

    personality = st.selectbox("AI Personality", [
        "Helpful Assistant",
        "Pakistan Cricket Expert",
        "Python Teacher",
        "Business Advisor"
    ])

    temperature = st.slider("Creativity", 0.0, 1.0, 0.7)

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"You are a {personality}. Reply clearly."
            }
        ]
        st.rerun()

# -------------------- CHAT DISPLAY --------------------
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="bot-msg">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- USER INPUT --------------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })


    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=st.session_state.messages
    )

        reply = response.choices[0].message.content

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption(f"Total Messages: {len(st.session_state.messages)}")
