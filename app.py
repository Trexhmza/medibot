import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv("gemini.env")
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please add it to gemini.env file.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="MediBot", page_icon="🩺", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .main-header {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        color: #a0a0b8;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .stChatMessage {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .stChatInput {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 25px;
    }
    .sidebar-content {
        padding: 1rem 0;
    }
    .model-badge {
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
        font-weight: 600;
    }
    footer {display: none}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.markdown("<h2 style='color: white; margin-top: 0;'>MediBot</h2>", unsafe_allow_html=True)
    st.markdown("<span class='model-badge'>llama-3.3-70b</span>", unsafe_allow_html=True)
    st.divider()

    st.markdown("**ℹ️ About**")
    st.info("MediBot provides general health information. Always consult a professional for medical advice.")

    st.divider()
    st.markdown("**⚙️ Options**")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**📋 Quick Questions**")
    import random
    all_qs = [
        "What are symptoms of dehydration?",
        "How to lower blood pressure naturally?",
        "What vitamins boost immunity?",
        "First aid for minor burns?",
        "Signs of a vitamin D deficiency?",
        "How to improve sleep quality?",
        "Foods high in iron?",
        "What helps with headaches?",
        "Benefits of drinking water?",
        "How to reduce stress naturally?",
        "Symptoms of food poisoning?",
        "What is normal blood sugar range?",
    ]
    qs = random.sample(all_qs, 4)
    for q in qs:
        if st.button(q, use_container_width=True):
            st.session_state.quick_q = q
    st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🩺 MediBot</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Medical Information Assistant — Not a substitute for professional advice</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_q" not in st.session_state:
    st.session_state.quick_q = None

for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🩺"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

sys_prompt = "You are a medical info assistant. Always include: 'This is for informational purposes only, not medical advice. In emergencies, contact your doctor or emergency services.' Do not diagnose or prescribe."

prompt = None
if st.session_state.quick_q:
    prompt = st.session_state.quick_q
    st.session_state.quick_q = None
else:
    prompt = st.chat_input("Ask your medical question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": prompt},
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
            except Exception as e:
                st.error(f"API error: {e}")
                reply = ""
    st.session_state.messages.append({"role": "assistant", "content": reply})
