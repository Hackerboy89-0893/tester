import streamlit as st
from groq import Groq
import uuid

# Page Config
st.set_page_config(page_title="NotBias.com", layout="wide")

# Modern SaaS CSS
st.markdown("""
<style>
    /* Reset & Base */
    .stApp { background-color: #f8fafc; }
    
    /* Navbar */
    .navbar { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; background: white; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; z-index: 1000; }
    .logo { font-weight: 800; font-size: 20px; color: #1f2937; }
    
    /* Hero */
    .hero { text-align: left; padding: 4rem 0; }
    .hero h1 { font-size: 3.5rem; font-weight: 800; color: #000; line-height: 1.1; margin-bottom: 1rem; }
    .hero span { color: #7c3aed; }
    .hero p { font-size: 1.25rem; color: #6b7280; max-width: 600px; }
    
    /* Cards */
    .ui-card { background: white; padding: 24px; border-radius: 16px; border: 1px solid #e5e7eb; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .card-left { border-left: 6px solid #10b981; }
    .card-right { border-left: 6px solid #3b82f6; }
    .card-data { border-left: 6px solid #f59e0b; background: #fffbeb; }
    .card-verdict { border-left: 6px solid #7c3aed; background: #faf5ff; }
    
    /* Input Area */
    .stChatInput { padding: 2rem 0; }
    
    /* Utility Labels */
    .label { font-size: 10px; font-weight: 800; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.1em; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# Navbar
st.markdown('<div class="navbar"><div class="logo">NotBias</div><div>How it works | Demo | Principles</div><button style="background:#7c3aed; color:white; border:none; padding:8px 16px; border-radius:8px;">Get Access</button></div>', unsafe_allow_html=True)

# State
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {"main": {"messages": []}}

# Main Layout
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="hero"><h1>The AI that <span>refuses</span> to take a side.</h1><p>NotBias steelmans every perspective, separates fact from value judgment, and tells you when something is contested.</p></div>', unsafe_allow_html=True)

with col_right:
    # Chat History
    for msg in st.session_state.chat_sessions["main"]["messages"]:
        st.markdown(f"**You:** {msg['user_q']}")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="label">Perspective A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ui-card card-left">{msg["p_a"]}</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="label">Perspective B</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ui-card card-right">{msg["p_b"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="label">Verdict</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-card card-verdict">{msg["verdict"]}</div>', unsafe_allow_html=True)

    # Input
    if user_query := st.chat_input("Ask a hard question..."):
        with st.spinner("Analyzing..."):
            # Groq Client Logic
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "Split into [START_PERSPECTIVE_A], [START_PERSPECTIVE_B], [START_VERDICT]"}, {"role": "user", "content": user_query}]
            )
            raw = completion.choices[0].message.content
            # Basic parsing logic here
            data = {"user_q": user_query, "p_a": "...", "p_b": "...", "verdict": "..."}
            st.session_state.chat_sessions["main"]["messages"].append(data)
            st.rerun()
