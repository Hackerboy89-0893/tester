import streamlit as st
from groq import Groq
import uuid

# 1. Page Config
st.set_page_config(page_title="NotBias.com Engine", layout="wide")

# 2. Styles
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #fafafa; color: #1e293b; font-family: 'Inter', sans-serif; }
    .ui-card { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .card-left { border-left: 4px solid #10b981; }
    .card-right { border-left: 4px solid #3b82f6; }
    .card-data { border-left: 4px solid #f59e0b; background: #f8fafc; }
    .card-verdict { border-top: 4px solid #a855f7; background: #faf5ff; margin-top: 15px; }
    .card-header { font-size: 11px; font-weight: 800; text-transform: uppercase; color: #64748b; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. State
if "chat_sessions" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {first_id: {"title": "⚖️ New Analysis", "messages": []}}
    st.session_state.active_session_id = first_id

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.stop()

# 4. Sidebar
with st.sidebar:
    st.title("NotBias.com")
    if st.button("➕ New Thread"):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "⚖️ New Analysis", "messages": []}
        st.session_state.active_session_id = new_id
        st.rerun()
    for sid, sdata in st.session_state.chat_sessions.items():
        if st.button(sdata["title"], key=sid):
            st.session_state.active_session_id = sid
            st.rerun()

# 5. Main Chat Logic
active_id = st.session_state.active_session_id
current_session = st.session_state.chat_sessions[active_id]

# DISPLAY HISTORY
for msg in current_session["messages"]:
    with st.chat_message("assistant", avatar="⚖️"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A</div></div>', unsafe_allow_html=True)
            st.markdown(msg["p_a"])
        with col2:
            st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B</div></div>', unsafe_allow_html=True)
            st.markdown(msg["p_b"])
        st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Baseline</div></div>', unsafe_allow_html=True)
        st.markdown(msg["baseline"])
        st.markdown(f'<div class="ui-card card-verdict"><div class="card-header">⚖️ Final Verdict</div>{msg["verdict"]}</div>', unsafe_allow_html=True)

# PROCESS NEW INPUT
if user_query := st.chat_input("Ask notbias.com..."):
    st.chat_message("user").markdown(user_query)
    
    tag_constitution = (
        "You are an uncompromisingly neutral observer. Split response into exactly 4 sections:\n"
        "[START_PERSPECTIVE_A]\n[START_PERSPECTIVE_B]\n[START_BASELINE]\n[START_VERDICT]"
    )
    
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Analyzing..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": tag_constitution}, {"role": "user", "content": user_query}]
            )
            raw = completion.choices[0].message.content
            
            # Parsing
            parts = {"p_a": "...", "p_b": "...", "baseline": "...", "verdict": "..."}
            try:
                s = raw.split("[START_PERSPECTIVE_A]")[1].split("[START_PERSPECTIVE_B]")
                parts["p_a"] = s[0]
                s2 = s[1].split("[START_BASELINE]")
                parts["p_b"] = s2[0]
                s3 = s2[1].split("[START_VERDICT]")
                parts["baseline"] = s3[0]
                parts["verdict"] = s3[1]
            except: parts["p_a"] = raw 
            
            # SAVE TO HISTORY THEN RERUN
            current_session["messages"].append(parts)
            current_session["title"] = f"💬 {user_query[:20]}..."
            st.rerun()
