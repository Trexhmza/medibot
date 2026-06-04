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
    ASSISTANT_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='50' fill='%23E63946'/%3E%3Ctext x='50' y='68' text-anchor='middle' font-size='50' fill='white'%3E🩺%3C/text%3E%3C/svg%3E"

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<style>
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(230, 57, 70, 0.5); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(230, 57, 70, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(230, 57, 70, 0); }
    }

    * { box-sizing: border-box; }

    .stApp {
        background: #050505 !important;
    }

    header[data-testid="stHeader"] {
        background: #0a0a0a !important;
        border-bottom: 1px solid #1a0a0a !important;
    }

    section[data-testid="stSidebar"] {
        background: #0d0d0d !important;
        border-right: 1px solid #1a0a0a !important;
        min-width: 280px !important;
        max-width: 320px !important;
    }
    section[data-testid="stSidebar"] > div { background: transparent !important; }
    div[data-testid="stSidebarUserContent"] { padding: 1rem 1rem 0 1rem !important; }

    .sidebar-brand {
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 1.5rem; padding: 0.25rem;
    }
    .sidebar-brand-icon {
        width: 44px; height: 44px; border-radius: 12px;
        background: linear-gradient(135deg, #E63946, #8B0000);
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .sidebar-brand-text h2 {
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 20px; font-weight: 700;
        color: #e5e2e1; margin: 0; line-height: 1.2;
    }
    .sidebar-brand-text p {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: #ab8987; margin: 0; letter-spacing: 0.05em;
    }

    .nav-btn {
        width: 100% !important;
        background: transparent !important;
        border: 1px solid #2a1212 !important;
        color: #e5e2e1 !important;
        font-family: 'Hanken Grotesk', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        text-align: left !important;
        transition: all 0.15s !important;
        margin: 3px 0 !important;
    }
    .nav-btn:hover {
        background: rgba(230, 57, 70, 0.05) !important;
        border-color: #E63946 !important;
    }

    .upgrade-btn {
        width: 100%; padding: 14px;
        background: linear-gradient(135deg, #E63946, #8B0000);
        color: white; font-family: 'Hanken Grotesk', sans-serif;
        font-weight: 700; font-size: 14px;
        border: none; border-radius: 8px;
        cursor: pointer; transition: opacity 0.2s;
        margin: 1rem 0;
    }
    .upgrade-btn:hover { opacity: 0.9; }

    .main-header {
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 28px; font-weight: 700;
        color: #e5e2e1; text-align: center;
        padding: 1rem 0 0.1rem 0;
        letter-spacing: -0.02em;
    }
    .main-header span {
        color: #E63946;
    }
    .sub-header {
        font-family: 'Hanken Grotesk', sans-serif;
        color: #ab8987; text-align: center;
        font-size: 0.85rem; margin-bottom: 1.5rem;
        font-weight: 400;
    }

    .stChatMessage {
        animation: fadeUp 0.3s ease-out forwards;
        margin: 0.5rem 0;
    }

    /* Assistant (bot) chat bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) > div:first-child {
        background: #1A1A1A !important;
        border-left: 4px solid #E63946 !important;
        border-radius: 0 8px 8px 8px !important;
        padding: 1rem 1.25rem !important;
        color: #e5e2e1 !important;
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 15px; line-height: 1.6;
        max-width: 82%;
        box-shadow: none !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
    }

    /* User chat bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        display: flex;
        justify-content: flex-end;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child {
        background: #2A1212 !important;
        border: none !important;
        border-radius: 8px 8px 0 8px !important;
        padding: 1rem 1.25rem !important;
        color: #e0e0e0 !important;
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 15px; line-height: 1.6;
        max-width: 82%;
        margin-left: auto;
        box-shadow: none !important;
    }

    /* Chat input */
    div[data-testid="stBottom"] > div {
        background: #0a0a0a !important;
        border-top: 1px solid #1a0a0a !important;
        padding: 0.75rem 1rem 1rem !important;
    }
    div[data-testid="stBottom"] > div > div {
        background: #121212 !important;
        border: 1px solid #2a1212 !important;
        border-radius: 8px !important;
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 2px !important;
        transition: border-color 0.2s !important;
    }
    div[data-testid="stBottom"] > div > div:focus-within {
        border-color: #E63946 !important;
        box-shadow: 0 0 12px rgba(230, 57, 70, 0.15) !important;
    }
    div[data-testid="stBottom"] textarea {
        font-family: 'Hanken Grotesk', sans-serif !important;
        font-size: 15px !important;
        color: #e5e2e1 !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 8px 12px !important;
    }
    div[data-testid="stBottom"] textarea::placeholder {
        color: #5b403f !important;
    }
    div[data-testid="stBottom"] button {
        background: #E63946 !important;
        border-radius: 6px !important;
        border: none !important;
        transition: all 0.15s !important;
        min-width: 40px !important;
        min-height: 40px !important;
    }
    div[data-testid="stBottom"] button:hover { background: #ff525b !important; }

    /* Sidebar buttons */
    .stSidebar .stButton button {
        width: 100% !important;
        background: transparent !important;
        border: 1px solid #2a1212 !important;
        color: #e5e2e1 !important;
        font-family: 'Hanken Grotesk', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        transition: all 0.15s !important;
    }
    .stSidebar .stButton button:hover {
        background: rgba(230, 57, 70, 0.05) !important;
        border-color: #E63946 !important;
    }

    .stSidebar .stInfo {
        font-family: 'Hanken Grotesk', sans-serif !important;
        font-size: 13px !important;
        background: #1a0a0a !important;
        border: 1px solid #2a1212 !important;
        color: #e4bebc !important;
    }

    .stSpinner > div { border-color: #E63946 !important; border-top-color: transparent !important; }

    .stSidebar hr {
        border-color: #1a0a0a !important;
        margin: 1rem 0 !important;
    }

    .stSidebar .sidebar-section-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        color: #ab8987;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
    }

    .spacer { height: 120px; }

    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
        }
        .spacer { height: 140px; }
        .main-header { font-size: 22px; }
        div[data-testid="stChatMessage"] > div:first-child {
            max-width: 90% !important;
        }
    }

    footer { display: none; }
    #MainMenu { visibility: hidden; }
    .stDeployButton { display: none !important; }

    .quick-q-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 500;
        color: #ab8987;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">
            <span class="material-symbols-outlined" style="color:white; font-size:24px;">smart_toy</span>
        </div>
        <div class="sidebar-brand-text">
            <h2>MediBot</h2>
            <p>Clinical Assistant</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ New Consultation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    if st.button("📋 Health History", use_container_width=True):
        st.info("Health history feature coming soon.")
    if st.button("📊 Insights", use_container_width=True):
        st.info("Insights feature coming soon.")
    if st.button("⚙️ Settings", use_container_width=True):
        st.info("Settings feature coming soon.")

    st.markdown("<button class='upgrade-btn'>Upgrade to Pro</button>", unsafe_allow_html=True)

    if st.button("❓ Help Center", use_container_width=True):
        st.info("Help center coming soon.")

    st.markdown("<div class='quick-q-label'>Quick Questions</div>", unsafe_allow_html=True)
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

st.markdown("<div class='main-header'>MediBot</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Medical Information Assistant — Not a substitute for professional advice</div>", unsafe_allow_html=True)

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
