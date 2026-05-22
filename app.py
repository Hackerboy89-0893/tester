import streamlit as st
from groq import Groq
import uuid

# 1. Page Config & Wide Layout (Crucial for dashboard sidebars)
st.set_page_config(page_title="NotBias.com Engine", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced Premium CSS UI Theme (ChatGPT Dark/Light-neutral aesthetic)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stMarkdownContainer"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }
    
    /* Sidebar styling adjustment */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Premium visual layout cards */
    .ui-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }
    .card-left { border-top: 4px solid #10b981; }  /* Green Perspective */
    .card-right { border-top: 4px solid #3b82f6; } /* Blue Perspective */
    .card-data { border-left: 4px solid #64748b; background-color: #f8fafc; } /* Slate Baseline */
    
    .card-header {
        font-size: 15px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #475569;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Initialize Global Application Session States
if "chat_sessions" not in st.session_state:
    # Structure: { session_id: { "title": "New Chat", "messages": [] } }
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
    st.title("⚖️ NotBias.com")
    st.caption("Machine Neutrality Panel v1.2")
    st.markdown("---")
    
    # Action Control: Create a brand new chat tab
    if st.button("➕ New Conversation Thread", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state.chat_sessions[new_id] = {"title": "⚖️ New Analysis", "messages": []}
        st.session_state.active_session_id = new_id
        st.parent_rerun() if hasattr(st, "parent_rerun") else st.rerun()

    st.markdown("<br><p style='font-size:12px; font-weight:600; color:#94a3b8;'>RECENT THREADS</p>", unsafe_allow_html=True)
    
    # Loop through and generate dynamic navigation tabs
    for session_id, session_data in list(st.session_state.chat_sessions.items()):
        # Highlight current active session visually using button types
        is_active = (session_id == st.session_state.active_session_id)
        btn_type = "secondary" if not is_active else "primary"
        
        # Truncate title strings neatly so they fit in sidebar menu options
        display_title = session_data["title"]
        if len(display_title) > 28:
            display_title = display_title[:25] + "..."
            
        if st.button(display_title, key=f"nav_{session_id}", use_container_width=True):
            st.session_state.active_session_id = session_id
            st.parent_rerun() if hasattr(st, "parent_rerun") else st.rerun()

# =====================================================================
# MAIN CHAT DESKTOP INTERFACE
# =====================================================================
active_id = st.session_state.active_session_id
current_session = st.session_state.chat_sessions[active_id]

# Welcoming layout display if chat history database log is empty
if not current_session["messages"]:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.subheader("Enter a controversial topic, historical question, or debate baseline.")
    st.info("The system will actively deploy multi-model adversarial checks to isolate confirmation bias and present structural data lines.")

# Render existing chat logs from storage for the active session
for msg in current_session["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A</div></div>', unsafe_allow_html=True)
                st.markdown(msg["p_a"])
            with col2:
                st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B</div></div>', unsafe_allow_html=True)
                st.markdown(msg["p_b"])
            st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Objective Metrics & Structural Baselines</div></div>', unsafe_allow_html=True)
            st.markdown(msg["baseline"])

# Accept new inputs from the clean floating input text tray line
if user_query := st.chat_input("Query the neutral matrix..."):
    # Immediately render your user query bubble onto screen
    st.chat_message("user").markdown(user_query)
    
    # Auto-rename the generic tab name to mirror your topic instantly
    if current_session["title"] in ["⚖️ New Analysis", "⚖️ First Neutral Analysis"]:
        current_session["title"] = f"⚖️ {user_query.strip().capitalize()}"
        
    # Commit your prompt trace into the persistent app structural storage history
    current_session["messages"].append({"role": "user", "content": user_query})
    
    # Central Neutrality Prompt Architecture Blueprint
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
    
    with st.chat_message("assistant"):
        with st.spinner("Processing framework nodes..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": tag_constitution},
                        {"role": "user", "content": user_query}
                    ]
                )
                
                raw_text = completion.choices[0].message.content
                p_a, p_b, baseline = "Processing failure.", "Processing failure.", "Processing failure."
                
                # Split algorithm mechanics parsing data cleanly outside risky JSON schemas
                if "[START_PERSPECTIVE_A]" in raw_text and "[START_PERSPECTIVE_B]" in raw_text and "[START_BASELINE]" in raw_text:
                    part_a_and_more = raw_text.split("[START_PERSPECTIVE_A]")[1]
                    p_a, remaining = part_a_and_more.split("[START_PERSPECTIVE_B]")
                    p_b, baseline = remaining.split("[START_BASELINE]")
                    p_a, p_b, baseline = p_a.strip(), p_b.strip(), baseline.strip()
                else:
                    p_a = raw_text
                
                # Render live visually onto dashboard space grids
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A</div></div>', unsafe_allow_html=True)
                    st.markdown(p_a)
                with col2:
                    st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B</div></div>', unsafe_allow_html=True)
                    st.markdown(p_b)
                st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Objective Metrics & Structural Baselines</div></div>', unsafe_allow_html=True)
                st.markdown(baseline)
                
                # Save structured output into persistent message logs state arrays 
                current_session["messages"].append({
                    "role": "assistant",
                    "p_a": p_a,
                    "p_b": p_b,
                    "baseline": baseline
                })
                
                # Force instant UI paint refresh sync cycle
                st.parent_rerun() if hasattr(st, "parent_rerun") else st.rerun()
                
            except Exception as e:
                st.error(f"Engine Core Disconnected: {e}")
