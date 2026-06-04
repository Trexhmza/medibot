import streamlit as st
from groq import Groq
import os
import random
from dotenv import load_dotenv
from streamlit.components.v1 import html as html_component

load_dotenv("gemini.env")
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please add it to gemini.env file.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="VitaAI Concierge", page_icon="🩺", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<style>
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(209, 242, 235, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(209, 242, 235, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(209, 242, 235, 0); }
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        background: #f8fafb;
    }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(209, 242, 235, 0.3) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(45, 125, 161, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(13, 59, 64, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    header[data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 40px rgba(45, 125, 161, 0.05) !important;
    }
    section[data-testid="stSidebar"] {
        background: rgba(248, 250, 251, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 40px 0 60px rgba(45, 125, 161, 0.03) !important;
    }
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 2rem;
        padding: 0 0.5rem;
    }
    .sidebar-brand-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, #2D7DA1, #D1F2EB);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 20px rgba(45, 125, 161, 0.2);
    }
    .sidebar-brand-text h2 {
        font-family: 'Montserrat', sans-serif;
        font-size: 24px;
        font-weight: 600;
        color: #0D3B40;
        margin: 0;
        line-height: 1.2;
    }
    .sidebar-brand-text p {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #2D7DA1;
        opacity: 0.7;
        margin: 0;
    }
    .main-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 32px !important;
        font-weight: 600 !important;
        color: #002428 !important;
        text-align: center;
        letter-spacing: 0.01em;
        padding: 1rem 0 0.25rem 0;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #414849;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    div[data-testid="stChatMessage"] {
        animation: fadeUp 0.4s ease-out forwards;
        margin: 0.5rem 0;
    }
    div[data-testid="stChatMessage"][data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        display: flex;
        justify-content: flex-end;
    }
    div[data-testid="stChatMessage"] > div:first-child {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 16px !important;
        padding: 1rem 1.25rem !important;
        color: #0D3B40 !important;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(45, 125, 161, 0.05) !important;
        max-width: 85%;
        margin-left: 0;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child {
        background: #0D3B40 !important;
        border: none !important;
        border-radius: 16px 16px 4px 16px !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(13, 59, 64, 0.15) !important;
        margin-left: auto;
        max-width: 85%;
    }
    .stChatFloatingInputContainer {
        background: transparent !important;
        padding-bottom: 1rem !important;
    }
    div[data-testid="stBottom"] > div {
        background: transparent !important;
        border: none !important;
        padding: 0 1rem 1rem 1rem !important;
    }
    div[data-testid="stBottom"] > div > div {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 9999px !important;
        box-shadow: 0 20px 50px rgba(45, 125, 161, 0.1) !important;
        padding: 0.25rem 0.25rem 0.25rem 1.25rem !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    div[data-testid="stBottom"] textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important;
        color: #0D3B40 !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 0.5rem 0 !important;
    }
    div[data-testid="stBottom"] textarea::placeholder {
        color: rgba(45, 125, 161, 0.4) !important;
    }
    div[data-testid="stBottom"] textarea:focus {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stBottom"] button {
        background: linear-gradient(135deg, #2D7DA1, #0D3B40) !important;
        border-radius: 9999px !important;
        border: none !important;
        box-shadow: 0 0 20px rgba(209, 242, 235, 0.4) !important;
        transition: all 0.2s !important;
        min-width: 48px !important;
        min-height: 48px !important;
    }
    div[data-testid="stBottom"] button:hover {
        transform: scale(1.05) !important;
    }
    div[data-testid="stBottom"] button:active {
        transform: scale(0.95) !important;
    }
    footer {display: none}
    .spacer { height: 100px; }
    @media (max-width: 768px) {
        .spacer { height: 120px; }
        .main-header { font-size: 24px !important; }
    }
    .stSidebar .stButton button {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        background: rgba(255,255,255,0.5) !important;
        color: #0D3B40 !important;
    }
    .stSidebar .stButton button:hover {
        background: rgba(209, 242, 235, 0.3) !important;
        border-color: rgba(45, 125, 161, 0.2) !important;
    }
    .stSidebar .stInfo {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        background: rgba(209, 242, 235, 0.2) !important;
        border: 1px solid rgba(209, 242, 235, 0.3) !important;
        color: #0D3B40 !important;
    }
    .stSpinner > div {
        border-color: #2D7DA1 !important;
    }
    div[data-testid="stStatusWidget"] {
        background: rgba(209, 242, 235, 0.4) !important;
        border-radius: 9999px !important;
        padding: 0.25rem 0.75rem !important;
        border: 1px solid #D1F2EB !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">
            <span class="material-symbols-outlined" style="color:white; font-variation-settings: 'FILL' 1;">medical_services</span>
        </div>
        <div class="sidebar-brand-text">
            <h2>Vita AI</h2>
            <p>Your Digital Specialist</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**ℹ️ About**")
    st.info("MediBot provides general health information. Always consult a professional for medical advice.")

    st.divider()
    st.markdown("**⚙️ Options**")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**📋 Quick Questions**")
    if "sample_qs" not in st.session_state:
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
        st.session_state.sample_qs = random.sample(all_qs, 4)
    for q in st.session_state.sample_qs:
        if st.button(q, use_container_width=True):
            st.session_state.quick_q = q
    st.divider()

st.markdown("<div class='main-header'>VitaAI Concierge</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Medical Information Assistant — Not a substitute for professional advice</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_q" not in st.session_state:
    st.session_state.quick_q = None

for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🩺"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

html_component("""
<script>
    const el = document.querySelector('[data-testid="stAppViewContainer"]');
    if (el) setTimeout(() => el.scrollTop = el.scrollHeight, 50);
</script>
""", height=0)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

sys_prompt = "You are a warm, caring nurse assistant. Speak with kindness and empathy like a real nurse would. If the user asks something off-topic (not health-related), gently steer them back — don't refuse bluntly. For example: 'That's an interesting question! While I'm here to help with health topics, is there something about your wellbeing I can assist with? 😊' Always include: 'This is for informational purposes only, not medical advice. In emergencies, contact your doctor or emergency services.' Never diagnose or prescribe."

prompt = st.chat_input("Ask your medical question...")
if st.session_state.quick_q:
    prompt = st.session_state.quick_q
    st.session_state.quick_q = None

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
