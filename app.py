import streamlit as st
from groq import Groq

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NotBias.com", layout="wide")

# --- 2. THEMES & STYLES ---
st.markdown("""
<style>
    :root { --accent: #7c3aed; }
    .stApp { background-color: #f8fafc; }
    .hero { max-width: 800px; margin: 40px auto 40px auto; text-align: center; }
    .hero h1 { font-size: 56px; font-weight: 800; color: #111827; line-height: 1.1; margin-bottom: 20px; }
    .hero h1 span { color: #7c3aed; }
    .hero p { font-size: 18px; color: #6b7280; line-height: 1.6; }
    .stats { display: flex; justify-content: center; gap: 40px; margin-bottom: 40px; font-family: monospace; font-size: 11px; color: #94a3b8; letter-spacing: 0.1em; }
    .ui-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .card-left { border-left: 5px solid #10b981; }
    .card-right { border-left: 5px solid #3b82f6; }
    .card-verdict { border-left: 5px solid #7c3aed; background: #faf5ff; }
    .label { font-size: 10px; font-weight: 800; text-transform: uppercase; color: #94a3b8; margin-bottom: 6px; }
</style>
""", unsafe_allow_html=True)

# --- 3. STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. HEADER ---
st.markdown("""
<div class="hero">
    <h1>The AI that gives you <span>every side</span> of the story.</h1>
    <p>Ask any contested question. Get the strongest case for every credible position — sourced, reasoned, and completely agenda-free.</p>
</div>
""", unsafe_allow_html=True)

# --- 5. CHAT DISPLAY & DYNAMIC CONTROLS ---
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message("user"):
        st.markdown(msg["user_q"])
    with st.chat_message("assistant"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="label">Perspective A</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ui-card card-left">{msg["p_a"]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="label">Perspective B</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="ui-card card-right">{msg["p_b"]}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="label">Decision Framework</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-card card-verdict">{msg["verdict"]}</div>', unsafe_allow_html=True)

        # Dynamic Controls
        b1, b2 = st.columns(2)
        if b1.button("Brief Summary", key=f"brief_{i}"):
            # Here you would trigger a rerun with a shorter prompt
            st.toast("Refining to brief...")
        if b2.button("Complex Analysis", key=f"complex_{i}"):
            st.toast("Deepening analysis...")
# 6. Process Input
if user_query := st.chat_input("Ask a hard question..."):
    # Initialize the data object here to guarantee it exists in the outer scope
    data = {"user_q": user_query, "p_a": "...", "p_b": "...", "verdict": "..."}
    
    if "complexity" not in st.session_state:
        st.session_state.complexity = "standard"
        
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Refining neutrality..."):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # Dynamic prompt injection
            mod = "Keep this response under 100 words." if st.session_state.complexity == "brief" else "Provide a detailed, technical analysis."
            
           system_prompt = f"""
You are the "NotBias Decision Lab". Provide a symmetrical analysis.
INSTRUCTION: {mod}

STRICT FORMATTING RULES:
You must output exactly these strings as standalone lines, with no other text on those lines:
[START_PERSPECTIVE_A]
[START_PERSPECTIVE_B]
[START_DECISION_FRAMEWORK]

- Do not include any headers like "Perspective A" or "Decision Framework" outside of those tags.
- For [START_DECISION_FRAMEWORK], provide a list where each item starts with a dash '-'.
- Use two newlines '\n\n' between items in the list to ensure they render correctly.
- Absolutely NO bolding (**).
"""
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            raw = completion.choices[0].message.content
            
            # Update the 'data' object based on API response
            try:
                idx_a = raw.find("[START_PERSPECTIVE_A]")
                idx_b = raw.find("[START_PERSPECTIVE_B]")
                idx_f = raw.find("[START_DECISION_FRAMEWORK]")
                
                if idx_a != -1 and idx_b > idx_a and idx_f > idx_b:
                    data["p_a"] = raw[idx_a + len("[START_PERSPECTIVE_A]"):idx_b].strip()
                    data["p_b"] = raw[idx_b + len("[START_PERSPECTIVE_B]"):idx_f].strip()
                    data["verdict"] = raw[idx_f + len("[START_DECISION_FRAMEWORK]"):].strip()
                else:
                    data["p_a"] = "Formatting error: The engine failed to separate the perspectives."
                    data["p_b"] = "Please try again."
                    data["verdict"] = "The response did not meet the required structural standards."
            except Exception as e:
                data["p_a"] = f"Technical Error: {str(e)}"
    
    # Now append is safe because data is guaranteed to exist
    st.session_state.messages.append(data)
    st.rerun()
