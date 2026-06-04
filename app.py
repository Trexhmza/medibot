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

USER_AVATAR = "WhatsApp Image 2026-06-05 at 2.51.33 AM.jpeg"
ASSISTANT_AVATAR = "Gemini_Generated_Image_q64wzmq64wzmq64w.png"

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
        display: none !important;
    }
    .stApp > div:first-child {
        margin-left: 0 !important;
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

    /* Avatar images - zoom/crop to remove whitespace */
    div[data-testid="chatAvatarIcon-assistant"] img,
    div[data-testid="chatAvatarIcon-user"] img {
        width: 40px !important;
        height: 40px !important;
        object-fit: cover !important;
        border-radius: 50% !important;
        border: 2px solid #2a1212 !important;
        transform: scale(1.3) !important;
    }
    div[data-testid="chatAvatarIcon-assistant"],
    div[data-testid="chatAvatarIcon-user"] {
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        overflow: hidden !important;
        border-radius: 50% !important;
    }

    /* User bubble - avatar on left, content on right */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) > div:first-child {
        background: #2A1212 !important;
        border: none !important;
        border-radius: 0 8px 8px 8px !important;
        padding: 1rem 1.25rem !important;
        color: #e0e0e0 !important;
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 15px; line-height: 1.6;
        max-width: 82%;
        box-shadow: none !important;
    }

    /* Assistant bubble - content on left, avatar on right */
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

    .stSpinner > div { border-color: #E63946 !important; border-top-color: transparent !important; }

    .spacer { height: 120px; }

    @media (max-width: 768px) {
        .spacer { height: 140px; }
        .main-header { font-size: 22px; }
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
#             <h2>MediBot</h2>
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

st.markdown("<div class='main-header'>MediBot</div>", unsafe_allow_html=True)
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
