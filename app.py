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

# --- 5. CHAT DISPLAY ---
for msg in st.session_state.messages:
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
        
        # This label now correctly matches your "Decision Framework" structure
        st.markdown('<div class="label">Decision Framework</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-card card-verdict">{msg["verdict"]}</div>', unsafe_allow_html=True)

# 6. Process Input
if user_query := st.chat_input("Ask a hard question..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Refining neutrality..."):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            system_prompt = """
You are the "NotBias Decision Lab". Your purpose is to provide a perfectly symmetrical analysis of any contested topic.

STRICT CONSTRAINTS:
1. NO VERDICTS. You do not provide a conclusion, opinion, or summary of who is 'right'.
2. PERFECT SYMMETRY. You must provide exactly TWO perspectives. Each must have similar length and clinical tone.
3. NO MARKDOWN BOLDING. Do not use ** or any other formatting characters for emphasis. Use plain text.
4. STEEL-MAN. Argue both positions as if you are the lead advocate for each.
5. FORMAT. Use exactly these labels, in this order:
[START_PERSPECTIVE_A]
[START_PERSPECTIVE_B]
[START_DECISION_FRAMEWORK]

For [START_DECISION_FRAMEWORK], provide a plain-text bulleted list (use a simple dash -) of the specific values, metrics, and criteria a user should weigh to decide between these two perspectives themselves.
"""
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            raw = completion.choices[0].message.content
            
            data = {"user_q": user_query, "p_a": "...", "p_b": "...", "verdict": "..."}
            
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
    
    st.session_state.messages.append(data)
    st.rerun()
