import streamlit as st
from groq import Groq
import os
import random
from pathlib import Path
from dotenv import load_dotenv
from streamlit.components.v1 import html as html_component

load_dotenv("gemini.env")
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please add it to gemini.env file.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(page_title="MediBot", page_icon="🩺", layout="wide")

ASSISTANT_AVATAR = None
for ext in ["png", "jpg", "jpeg", "webp"]:
    p = Path(f"assistant.{ext}")
    if p.exists():
        ASSISTANT_AVATAR = str(p)
        break
if not ASSISTANT_AVATAR:
    ASSISTANT_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%232D7DA1'/%3E%3Ctext x='50' y='68' text-anchor='middle' font-size='50' fill='white'%3E🩺%3C/text%3E%3C/svg%3E"

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
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    .stApp { background: #f8fafb; }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(209, 242, 235, 0.3) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(45, 125, 161, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(13, 59, 64, 0.05) 0%, transparent 50%);
        pointer-events: none; z-index: 0;
    }

    header[data-testid="stHeader"] {
        background: rgba(255,255,255,0.3) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255,255,255,0.3) !important;
        box-shadow: 0 4px 40px rgba(45,125,161,0.05) !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(248,250,251,0.5) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255,255,255,0.3) !important;
        box-shadow: 40px 0 60px rgba(45,125,161,0.03) !important;
        width: 320px !important;
    }
    section[data-testid="stSidebar"] > div { background: transparent !important; }
    div[data-testid="stSidebarUserContent"] { padding-top: 0 !important; }

    .sidebar-brand {
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 1.5rem; padding: 0.5rem 0.5rem 0 0.5rem;
    }
    .sidebar-brand-icon {
        width: 48px; height: 48px; border-radius: 12px;
        background: linear-gradient(135deg, #2D7DA1, #D1F2EB);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 8px 20px rgba(45,125,161,0.2);
    }
    .sidebar-brand-text h2 {
        font-family: 'Montserrat', sans-serif; font-size: 22px;
        font-weight: 600; color: #0D3B40; margin: 0; line-height: 1.2;
    }
    .sidebar-brand-text p {
        font-family: 'Inter', sans-serif; font-size: 13px;
        color: #2D7DA1; opacity: 0.7; margin: 0;
    }
    .nav-item {
        display: flex; align-items: center; gap: 12px;
        padding: 12px 16px; border-radius: 12px;
        font-family: 'Inter', sans-serif; font-size: 14px;
        color: #414849; cursor: pointer; transition: all 0.2s;
        border: none; background: transparent; width: 100%;
        text-align: left; margin: 2px 0;
    }
    .nav-item:hover { background: rgba(255,255,255,0.5); }
    .nav-item.active {
        background: rgba(209,242,235,0.3); color: #0D3B40; font-weight: 600;
    }
    .nav-item .icon { color: #2D7DA1; }
    .upgrade-btn {
        width: 100%; padding: 16px;
        background: linear-gradient(135deg, #2D7DA1, #0D3B40);
        color: white; font-family: 'Inter', sans-serif;
        font-weight: 700; font-size: 14px;
        border: none; border-radius: 12px;
        cursor: pointer; transition: opacity 0.2s;
        box-shadow: 0 8px 25px rgba(45,125,161,0.3);
        margin: 1rem 0;
    }
    .upgrade-btn:hover { opacity: 0.9; }

    .custom-topbar {
        display: flex; align-items: center; justify-content: space-between;
        padding: 12px 24px;
        background: rgba(255,255,255,0.3);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 4px 40px rgba(45,125,161,0.05);
        position: sticky; top: 0; z-index: 99;
    }
    .topbar-left { display: flex; align-items: center; gap: 12px; }
    .topbar-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 20px; font-weight: 700; color: #002428;
    }
    .topbar-right { display: flex; align-items: center; gap: 16px; }
    .topbar-status {
        display: flex; align-items: center; gap: 6px;
        padding: 4px 14px; background: rgba(209,242,235,0.4);
        border-radius: 9999px; border: 1px solid #D1F2EB;
        font-family: 'Inter', sans-serif; font-size: 11px;
        font-weight: 700; color: #0D3B40;
        text-transform: uppercase; letter-spacing: 0.1em;
    }
    .topbar-status .dot {
        width: 8px; height: 8px; background: #D1F2EB;
        border-radius: 50%; animation: pulse 2s infinite;
    }
    .topbar-icon {
        width: 40px; height: 40px; border-radius: 50%;
        background: rgba(255,255,255,0.5);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; transition: background 0.2s;
    }
    .topbar-icon:hover { background: rgba(255,255,255,0.8); }
    .topbar-avatar {
        width: 40px; height: 40px; border-radius: 50%;
        background: linear-gradient(135deg, #D1F2EB, #2D7DA1);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; font-size: 18px;
        box-shadow: 0 2px 8px rgba(45,125,161,0.15);
    }

    .chat-area {
        max-width: 800px; margin: 0 auto; padding: 1rem 1rem 0 1rem;
    }
    .stChatMessage { animation: fadeUp 0.4s ease-out forwards; }

    div[data-testid="stChatMessage"] > div:first-child {
        background: rgba(255,255,255,0.85) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
        border-radius: 16px 16px 16px 4px !important;
        padding: 1rem 1.25rem !important;
        color: #0D3B40 !important;
        font-family: 'Inter', sans-serif; font-size: 15px; line-height: 1.6;
        box-shadow: 0 4px 15px rgba(45,125,161,0.05) !important;
        max-width: 85%; position: relative; overflow: hidden;
    }
    div[data-testid="stChatMessage"] > div:first-child::after {
        content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        border: 1px solid transparent;
        background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 50%, rgba(255,255,255,0.1) 100%) border-box;
        -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
        mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: destination-out;
        mask-composite: exclude;
        pointer-events: none;
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child {
        background: #0D3B40 !important;
        border: none !important;
        border-radius: 16px 16px 4px 16px !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(13,59,64,0.15) !important;
        margin-left: auto; max-width: 85%;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child::after {
        display: none !important;
    }

    .stChatFloatingInputContainer { background: transparent !important; padding-bottom: 0 !important; }
    div[data-testid="stBottom"] > div {
        background: transparent !important; border: none !important;
        padding: 0 1rem 1.5rem !important;
    }
    div[data-testid="stBottom"] > div > div {
        background: rgba(255,255,255,0.7) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 9999px !important;
        box-shadow: 0 20px 50px rgba(45,125,161,0.1) !important;
        padding: 4px 4px 4px 20px !important;
        max-width: 800px !important; margin: 0 auto !important;
    }
    div[data-testid="stBottom"] textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 16px !important; color: #0D3B40 !important;
        background: transparent !important; border: none !important;
        outline: none !important; box-shadow: none !important;
        padding: 8px 0 !important;
    }
    div[data-testid="stBottom"] textarea::placeholder {
        color: rgba(45,125,161,0.4) !important;
    }
    div[data-testid="stBottom"] button {
        background: linear-gradient(135deg, #2D7DA1, #0D3B40) !important;
        border-radius: 9999px !important; border: none !important;
        box-shadow: 0 0 20px rgba(209,242,235,0.4) !important;
        transition: all 0.2s !important;
        min-width: 48px !important; min-height: 48px !important;
    }
    div[data-testid="stBottom"] button:hover { transform: scale(1.05) !important; }
    div[data-testid="stBottom"] button:active { transform: scale(0.95) !important; }

    .stSidebar .stButton button {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important; transition: all 0.2s !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        background: rgba(255,255,255,0.5) !important;
        color: #0D3B40 !important;
    }
    .stSidebar .stButton button:hover {
        background: rgba(209,242,235,0.3) !important;
        border-color: rgba(45,125,161,0.2) !important;
    }
    .stSidebar .stInfo {
        font-family: 'Inter', sans-serif !important; font-size: 14px !important;
        background: rgba(209,242,235,0.2) !important;
        border: 1px solid rgba(209,242,235,0.3) !important;
        color: #0D3B40 !important;
    }
    .stSpinner > div { border-color: #2D7DA1 !important; }
    .spacer { height: 120px; }
    @media (max-width: 768px) {
        .spacer { height: 140px; }
        .custom-topbar { padding: 10px 16px; }
        .topbar-status span { display: none; }
    }
    footer { display: none; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">
            <span class="material-symbols-outlined" style="color:white; font-variation-settings:'FILL' 1;">medical_services</span>
        </div>
        <div class="sidebar-brand-text">
            <h2>MediBot</h2>
            <p>Your Health Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ New Consultation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("📋 Health History", use_container_width=True):
        st.info("Health history feature coming soon.")
    if st.button("📊 Medical Insights", use_container_width=True):
        st.info("Medical insights feature coming soon.")
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("Settings feature coming soon.")

    st.markdown("<button class='upgrade-btn'>Upgrade to Pro</button>", unsafe_allow_html=True)

    if st.button("❓ Help Center", use_container_width=True):
        st.info("Help center coming soon.")

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

st.markdown("""
<div class="custom-topbar">
    <div class="topbar-left">
        <span class="material-symbols-outlined" style="color:#2D7DA1; font-size:28px;">smart_toy</span>
        <span class="topbar-title">MediBot</span>
    </div>
    <div class="topbar-right">
        <div class="topbar-status">
            <div class="dot"></div>
            <span>System Live</span>
        </div>
        <div class="topbar-icon">
            <span class="material-symbols-outlined" style="color:#2D7DA1;">notifications</span>
        </div>
        <div class="topbar-avatar">👤</div>
    </div>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_q" not in st.session_state:
    st.session_state.quick_q = None

for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else ASSISTANT_AVATAR
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

prompt = st.chat_input("Describe your symptoms or ask a health question...")
if st.session_state.quick_q:
    prompt = st.session_state.quick_q
    st.session_state.quick_q = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
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
