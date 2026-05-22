import streamlit as st
from groq import Groq
import uuid

# 1. Page Config & Layout Architecture
st.set_page_config(page_title="NotBias.com Engine", layout="wide", initial_sidebar_state="expanded")

# 2. Premium AI Chatbot Interface Dark Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Root App Canvas Remap */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d14 !important;
        color: #f1f5f9 !important;
    }
    
    /* Native Sidebar Restyling */
    [data-testid="stSidebar"] {
        background-color: #131622 !important;
        border-right: 1px solid #22293f !important;
    }
    
    /* Dynamic Buttons & Workspace Selectors */
    .stButton > button {
        background-color: #1e2538 !important;
        color: #e2e8f0 !important;
        border: 1px solid #2e3956 !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #2b354f !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    /* Active Thread Navigation Button Highlight Overrides */
    div[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* Native Chat Container Width Overrides to look like a desktop app */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.5rem 0rem !important;
    }
    
    /* Premium Glassmorphism UI Cards inside the Assistant rows */
    .ui-card {
        background: rgba(25, 30, 48, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        margin-top: 10px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }
    
    /* Perspective Card Accents */
    .card-left { border-top: 4px solid #10b981; }  
    .card-right { border-top: 4px solid #3b82f6; } 
    .card-data { border-left: 4px solid #f59e0b; background: rgba(30, 35, 54, 0.4); } 
    
    .card-header {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        margin-bottom: 10px;
    }

    /* Clean Floating Text Tray Anchor adjustments */
    [data-testid="stChatInput"] {
        background-color: #131622 !important;
        border: 1px solid #2d3748 !important;
        border-radius: 14px !important;
    }
    
    /* Global Markdown Text Coloring Fixes */
    h1, h2, h3, h4, p, li, span {
        color: #f1f5f9 !important;
    }
    strong {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Global Application Session States
if "chat_sessions" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {
        first_id: {"title": "⚖️ First Neutral Analysis", "messages": []}
    }
    st.session_state.active_session_id = first_id

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("Infrastructure Error: Secure API Key missing in Streamlit Secrets setup.")
    st.stop()

# =====================================================================
# SIDEBAR NAVIGATION (THE CHAT TABS AND HISTORY)
# =====================================================================
with st.sidebar:
    st.markdown("<h2 style='font-size:22px; font-weight:700; margin-bottom:4px;'>NotBias.com</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; color:#64748b; margin-bottom:20px;'>Neural Architecture v2.0</p>", unsafe_allow_html=True)
    
    # Create a brand new workspace chat session 
    if st.button("➕ New Thread", use_container_width=True, type="secondary"):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "⚖️ New Analysis", "messages": []}
        st.session_state.active_session_id = new_id
        st.rerun()

    st.markdown("<br><p style='font-size:11px; font-weight:700; color:#475569; letter-spacing:0.08em;'>CONVERSATIONS</p>", unsafe_allow_html=True)
    
    # Render loop to paint history navigation lists
    for session_id, session_data in list(st.session_state.chat_sessions.items()):
        is_active = (session_id == st.session_state.active_session_id)
        btn_type = "primary" if is_active else "secondary"
        
        display_title = session_data["title"]
        if len(display_title) > 26:
            display_title = display_title[:23] + "..."
            
        if st.button(display_title, key=f"nav_{session_id}", use_container_width=True, type=btn_type):
            st.session_state.active_session_id = session_id
            st.rerun()

# =====================================================================
# MAIN CHAT DESKTOP INTERFACE
# =====================================================================
active_id = st.session_state.active_session_id
current_session = st.session_state.chat_sessions[active_id]

# Minimalist Welcome Board (ChatGPT/Gemini Style Startup Node)
if not current_session["messages"]:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 36px; font-weight: 700; background: linear-gradient(135deg, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>What can I balance for you today?</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 15px;'>Enter any highly controversial topic or debate to extract real-time adversarial framework perspectives.</p>", unsafe_allow_html=True)

# Render existing chat logs natively from history state
for msg in current_session["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        # CHATBOT DESIGN FIX: Wrapping the split layout completely inside a native assistant container bubble
        with st.chat_message("assistant", avatar="⚖️"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A (Interventionist / Reformist)</div></div>', unsafe_allow_html=True)
                st.markdown(msg["p_a"])
            with col2:
                st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B (Traditionalist / Free-Market)</div></div>', unsafe_allow_html=True)
                st.markdown(msg["p_b"])
            st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Objective Metrics & Structural Baselines</div></div>', unsafe_allow_html=True)
            st.markdown(msg["baseline"])

# Floating Input Processing Logic Triggers
if user_query := st.chat_input("Ask notbias.com..."):
    # Render user query right into the live stream
    st.chat_message("user").markdown(user_query)
    
    # Auto-rename the chat thread button tab
    if current_session["title"] in ["⚖️ New Analysis", "⚖️ First Neutral Analysis"]:
        current_session["title"] = f"💬 {user_query.strip().capitalize()}"
        
    current_session["messages"].append({"role": "user", "content": user_query})
    
    tag_constitution = (
        "You are an uncompromisingly neutral observer for NotBias.com.\n\n"
        "Analyze the user's prompt and split your response into exactly three sections "
        "separated by these exact uppercase system tags:\n"
        "[START_PERSPECTIVE_A]\n"
        "[START_PERSPECTIVE_B]\n"
        "[START_BASELINE]\n\n"
        "CRITICAL ARCHITECTURE RULES:\n"
        "1. Never write running paragraphs or narrative summaries. Everything must be short, punchy micro-bullets.\n"
        "2. Every bullet point must start with an explicit **Bold Key Phrase Anchor** tracking the core argument data point.\n"
        "3. Provide equal space and matching tone weights to both Perspective sides.\n"
        "4. Treat Perspective A as the progressive, interventionist, or change-focused side, and Perspective B as the conservative, traditional, or free-market side where applicable."
    )
    
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Isolating spectrum markers..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": tag_constitution},
                        {"role": "user", "content": user_query}
                    ]
                )
                
                raw_text = completion.choices[0].message.content
                
                # Adaptive Parsing Block
                p_a, p_b, baseline = "No data generated.", "No data generated.", "No data generated."
                
                if "[START_PERSPECTIVE_A]" in raw_text:
                    remainder_a = raw_text.split("[START_PERSPECTIVE_A]", 1)[1]
                else:
                    remainder_a = raw_text

                if "[START_PERSPECTIVE_B]" in remainder_a:
                    p_a, remainder_b = remainder_a.split("[START_PERSPECTIVE_B]", 1)
                else:
                    p_a = remainder_a
                    remainder_b = ""

                if "[START_BASELINE]" in remainder_b:
                    p_b, baseline = remainder_b.split("[START_BASELINE]", 1)
                else:
                    p_b = remainder_b
                
                p_a, p_b, baseline = p_a.strip(), p_b.strip(), baseline.strip()
                
                # Render live inside the active live streaming thread row
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A (Interventionist / Reformist)</div></div>', unsafe_allow_html=True)
                    st.markdown(p_a)
                with col2:
                    st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B (Traditionalist / Free-Market)</div></div>', unsafe_allow_html=True)
                    st.markdown(p_b)
                st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Objective Metrics & Structural Baselines</div></div>', unsafe_allow_html=True)
                st.markdown(baseline)
                
                # Save structured history
                current_session["messages"].append({
                    "role": "assistant",
                    "p_a": p_a,
                    "p_b": p_b,
                    "baseline": baseline
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Engine Core Disconnected: {e}")
