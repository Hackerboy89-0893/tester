import streamlit as st
from groq import Groq
import uuid

# 1. Page Config
st.set_page_config(page_title="NotBias.com", layout="wide")

# 2. Refined Modern UI Styles
st.markdown("""
# 2. Refined Modern UI Styles
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc;
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }

    .ui-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    .card-left { border-left: 5px solid #10b981; }
    .card-right { border-left: 5px solid #3b82f6; }
    .card-data { border-left: 5px solid #f59e0b; background: #fffbeb; }
    .card-verdict { border-left: 5px solid #c084fc; background: #faf5ff; }

    .header-label {
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        color: #94a3b8;
        margin-bottom: 8px;
        letter-spacing: 0.05em;
    }

    /* Input box styling like the screenshot */
    .stTextInput>div>div>input {
        border-radius: 16px;
        padding: 12px 16px;
        border: 1px solid #e5e7eb;
        font-size: 14px;
        color: #1e293b;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 16px;
        padding: 10px 24px;
        background-color: #7c3aed;
        color: #fff;
        font-weight: 600;
        border: none;
    }

    .stButton>button:hover {
        background-color: #6b21a8;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# 3. State Management
if "chat_sessions" not in st.session_state:
    first_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {first_id: {"title": "New Analysis", "messages": []}}
    st.session_state.active_session_id = first_id

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except: st.stop()

# 4. Sidebar Logic
with st.sidebar:
    st.markdown("## NotBias.com")
    if st.button("➕ New Thread", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "New Analysis", "messages": []}
        st.session_state.active_session_id = new_id
        st.rerun()
    st.divider()
    for sid, sdata in st.session_state.chat_sessions.items():
        if st.button(sdata["title"], key=sid, use_container_width=True):
            st.session_state.active_session_id = sid
            st.rerun()

# 5. Main Chat Display (Updated with safety checks)
active_id = st.session_state.active_session_id
current_session = st.session_state.chat_sessions[active_id]

# Show all history
for msg in current_session["messages"]:
    # Use .get() to prevent KeyError if data format is old
    with st.chat_message("user"):
        st.markdown(msg.get("user_q", "User query"))
        
    with st.chat_message("assistant"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="header-label">Perspective A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ui-card card-left">{msg.get("p_a", "...")}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="header-label">Perspective B</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ui-card card-right">{msg.get("p_b", "...")}</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="header-label">Baseline Facts</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-card card-data">{msg.get("baseline", "...")}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="header-label">Final Verdict</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-card card-verdict">{msg.get("verdict", "...")}</div>', unsafe_allow_html=True)

# 6. Process Input
if user_query := st.chat_input("Ask about any topic..."):
    # Display user immediately
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Refining neutrality..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "Split response into [START_PERSPECTIVE_A], [START_PERSPECTIVE_B], [START_BASELINE], [START_VERDICT]"}, 
                          {"role": "user", "content": user_query}]
            )
            raw = completion.choices[0].message.content
            
            # Simple Parser
            data = {"user_q": user_query, "p_a": "...", "p_b": "...", "baseline": "...", "verdict": "..."}
            try:
                s = raw.split("[START_PERSPECTIVE_A]")[1].split("[START_PERSPECTIVE_B]")
                data["p_a"] = s[0]
                s2 = s[1].split("[START_BASELINE]")
                data["p_b"] = s2[0]
                s3 = s2[1].split("[START_VERDICT]")
                data["baseline"] = s3[0]
                data["verdict"] = s3[1]
            except: data["p_a"] = raw
            
            current_session["messages"].append(data)
            current_session["title"] = user_query[:25]
            st.rerun()
