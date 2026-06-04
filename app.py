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

st.set_page_config(page_title="Heal Buddy", page_icon="🩺", layout="wide")

USER_AVATAR = "WhatsApp Image 2026-06-05 at 2.51.33 AM.jpeg"
ASSISTANT_AVATAR = "Gemini_Generated_Image_q64wzmq64wzmq64w.png"

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
<style>
    @keyframes bgShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px) scale(0.96); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 0 8px rgba(230, 57, 70, 0.2); }
        50% { box-shadow: 0 0 20px rgba(230, 57, 70, 0.4); }
    }
    @keyframes dotPulse {
        0%, 80%, 100% { transform: scale(0.6); opacity: 0.3; }
        40% { transform: scale(1); opacity: 1; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }

    * { box-sizing: border-box; }

    .stApp {
        background: #050505 !important;
    }
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse at 10% 20%, rgba(230, 57, 70, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 80%, rgba(139, 0, 0, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 50%, rgba(10, 10, 10, 0.5) 0%, transparent 100%);
        background-size: 200% 200%;
        animation: bgShift 20s ease-in-out infinite;
        pointer-events: none; z-index: 0;
    }

    header[data-testid="stHeader"] {
        background: rgba(10, 10, 10, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(230, 57, 70, 0.1) !important;
    }

    section[data-testid="stSidebar"] { display: none !important; }
    .stApp > div:first-child { margin-left: 0 !important; }

    .main-header {
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 32px; font-weight: 800;
        text-align: center;
        padding: 1.2rem 0 0.1rem 0;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #ff6b6b, #E63946, #ff6b6b);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: shimmer 4s linear infinite;
        position: relative;
        z-index: 1;
    }
    .main-header::after {
        content: 'Heal Buddy';
        position: absolute;
        top: 1.2rem; left: 0; right: 0;
        font-size: 32px; font-weight: 800;
        background: linear-gradient(135deg, transparent 20%, rgba(230, 57, 70, 0.1) 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: blur(12px);
        z-index: -1;
    }
    .sub-header {
        font-family: 'Hanken Grotesk', sans-serif;
        color: rgba(171, 137, 135, 0.6);
        text-align: center;
        font-size: 0.8rem;
        margin-bottom: 1.5rem;
        font-weight: 300;
        letter-spacing: 0.02em;
        position: relative;
        z-index: 1;
    }

    .stChatMessage {
        animation: slideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        margin: 0.6rem 0;
        position: relative;
        z-index: 1;
    }

    /* Avatars */
    div[data-testid="chatAvatarIcon-assistant"],
    div[data-testid="chatAvatarIcon-user"] {
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        overflow: hidden !important;
        border-radius: 50% !important;
        box-shadow: 0 0 0 2px rgba(230, 57, 70, 0.15), 0 4px 12px rgba(0,0,0,0.4) !important;
        transition: transform 0.2s !important;
    }
    div[data-testid="chatAvatarIcon-assistant"]:hover,
    div[data-testid="chatAvatarIcon-user"]:hover {
        transform: scale(1.1) !important;
    }
    div[data-testid="chatAvatarIcon-assistant"] img,
    div[data-testid="chatAvatarIcon-user"] img {
        width: 42px !important;
        height: 42px !important;
        object-fit: cover !important;
        transform: scale(1.4) !important;
    }

    /* User bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child {
        background: linear-gradient(135deg, rgba(42, 18, 18, 0.95), rgba(30, 12, 12, 0.95)) !important;
        border: 1px solid rgba(230, 57, 70, 0.12) !important;
        border-radius: 0 14px 14px 14px !important;
        padding: 1rem 1.25rem !important;
        color: #e8e0e0 !important;
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 15px; line-height: 1.65;
        max-width: 82%;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(230, 57, 70, 0.08) !important;
    }

    /* Assistant bubble */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) > div:first-child {
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95), rgba(18, 18, 18, 0.95)) !important;
        border-left: 3px solid #E63946 !important;
        border-radius: 0 14px 14px 14px !important;
        padding: 1rem 1.25rem !important;
        color: #ece8e8 !important;
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 15px; line-height: 1.65;
        max-width: 82%;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
        animation: glowPulse 3s ease-in-out infinite !important;
        border-top: none !important;
        border-right: none !important;
        border-bottom: none !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) > div:first-child:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(230, 57, 70, 0.12) !important;
    }

    /* Chat input */
    div[data-testid="stBottom"] > div {
        background: linear-gradient(0deg, rgba(5,5,5,0.98) 0%, rgba(10,10,10,0.9) 100%) !important;
        border-top: 1px solid rgba(230, 57, 70, 0.08) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 0.75rem 1rem 1rem !important;
    }
    div[data-testid="stBottom"] > div > div {
        background: rgba(18, 18, 18, 0.8) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(230, 57, 70, 0.15) !important;
        border-radius: 12px !important;
        max-width: 800px !important;
        margin: 0 auto !important;
        padding: 3px !important;
        transition: all 0.3s !important;
    }
    div[data-testid="stBottom"] > div > div:focus-within {
        border-color: rgba(230, 57, 70, 0.5) !important;
        box-shadow: 0 0 20px rgba(230, 57, 70, 0.1), 0 0 60px rgba(230, 57, 70, 0.05) !important;
    }
    div[data-testid="stBottom"] textarea {
        font-family: 'Hanken Grotesk', sans-serif !important;
        font-size: 15px !important;
        color: #e5e2e1 !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
        padding: 10px 14px !important;
    }
    div[data-testid="stBottom"] textarea::placeholder {
        color: rgba(91, 64, 63, 0.6) !important;
        font-weight: 300 !important;
    }
    div[data-testid="stBottom"] button {
        background: linear-gradient(135deg, #E63946, #8B0000) !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.2s !important;
        min-width: 42px !important;
        min-height: 42px !important;
        animation: glowPulse 3s ease-in-out infinite !important;
    }
    div[data-testid="stBottom"] button:hover {
        background: linear-gradient(135deg, #ff525b, #a00000) !important;
        transform: scale(1.05) !important;
        animation: none !important;
        box-shadow: 0 0 25px rgba(230, 57, 70, 0.3) !important;
    }

    .stSpinner > div {
        border-color: rgba(230, 57, 70, 0.3) !important;
        border-top-color: #E63946 !important;
        border-width: 3px !important;
        width: 28px !important;
        height: 28px !important;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(230, 57, 70, 0.2);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(230, 57, 70, 0.4); }

    .spacer { height: 120px; }

    @media (max-width: 768px) {
        .spacer { height: 140px; }
        .main-header { font-size: 24px; }
        .main-header::after { font-size: 24px; top: 1.2rem; }
        div[data-testid="stChatMessage"] > div:first-child {
            max-width: 90% !important;
        }
    }

    footer { display: none; }
    #MainMenu { visibility: hidden; }
    .stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# with st.sidebar:
#     st.markdown("""
#     <div class="sidebar-brand">
#         <div class="sidebar-brand-icon">
#             <span class="material-symbols-outlined" style="color:white; font-size:24px;">smart_toy</span>
#         </div>
#         <div class="sidebar-brand-text">
#             <h2>Heal Buddy</h2>
#             <p>Clinical Assistant</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     if st.button("➕ New Consultation", use_container_width=True):
#         st.session_state.messages = []
#         st.rerun()
#     if st.button("📋 Health History", use_container_width=True):
#         st.info("Health history feature coming soon.")
#     if st.button("📊 Insights", use_container_width=True):
#         st.info("Insights feature coming soon.")
#     if st.button("⚙️ Settings", use_container_width=True):
#         st.info("Settings feature coming soon.")
#     st.markdown("<button class='upgrade-btn'>Upgrade to Pro</button>", unsafe_allow_html=True)
#     if st.button("❓ Help Center", use_container_width=True):
#         st.info("Help center coming soon.")
#     st.markdown("<div class='quick-q-label'>Quick Questions</div>", unsafe_allow_html=True)
#     if "sample_qs" not in st.session_state:
#         all_qs = [
#             "What are symptoms of dehydration?",
#             "How to lower blood pressure naturally?",
#             "What vitamins boost immunity?",
#             "First aid for minor burns?",
#             "Signs of a vitamin D deficiency?",
#             "How to improve sleep quality?",
#             "Foods high in iron?",
#             "What helps with headaches?",
#             "Benefits of drinking water?",
#             "How to reduce stress naturally?",
#             "Symptoms of food poisoning?",
#             "What is normal blood sugar range?",
#         ]
#         st.session_state.sample_qs = random.sample(all_qs, 4)
#     for q in st.session_state.sample_qs:
#         if st.button(q, use_container_width=True):
#             st.session_state.quick_q = q

st.markdown("<div class='main-header'>Heal Buddy</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Medical Information Assistant — Not a substitute for professional advice</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_q" not in st.session_state:
    st.session_state.quick_q = None

for msg in st.session_state.messages:
    avatar = USER_AVATAR if msg["role"] == "user" else ASSISTANT_AVATAR
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
    with st.chat_message("user", avatar=USER_AVATAR):
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
