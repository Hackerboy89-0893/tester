import streamlit as st
from groq import Groq
import uuid

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="NotBias.com", layout="wide")

# --- 2. THEMES & STYLES ---
st.markdown("""
<style>
    :root { --accent: #7c3aed; }
    .stApp { background-color: #f8fafc; }
    
    /* Hero Section */
    .hero { max-width: 800px; margin: 40px auto 40px auto; text-align: center; }
    .hero h1 { font-size: 56px; font-weight: 800; color: #111827; line-height: 1.1; margin-bottom: 20px; }
    .hero h1 span { color: #7c3aed; }
    .hero p { font-size: 18px; color: #6b7280; line-height: 1.6; }
    
    /* Stats */
    .stats { display: flex; justify-content: center; gap: 40px; margin-bottom: 40px; font-family: monospace; font-size: 11px; color: #94a3b8; letter-spacing: 0.1em; }
    
    /* Cards */
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

# --- 4. HEADER / HERO ---
st.markdown("""
<div class="hero">
    <h1>The AI that gives you <span>every side</span> of the story.</h1>
    <p>Ask any contested question. Get the strongest case for every credible position — sourced, reasoned, and completely agenda-free.</p>
</div>
<div class="stats">
    <span>0 OPINIONS HELD</span>
    <span>2+ SIDES PER ANSWER</span>
    <span>100% SOURCE-CITED</span>
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
        st.markdown('<div class="label">Final Verdict</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="ui-card card-verdict">{msg["verdict"]}</div>', unsafe_allow_html=True)

# 6. Process Input
if user_query := st.chat_input("Ask a hard question..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Refining neutrality..."):
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
            # --- UPDATED SYSTEM PROMPT ---
            system_prompt = """
            You are the "NotBias Neutrality Engine". Your sole purpose is to deconstruct contested questions into two opposing, high-quality, 'steel-man' arguments.

            STRICT CONSTRAINTS:
            1. NO conversational filler. Do not say "Certainly", "Here are the sides", or "It is important to note".
            2. ABSOLUTE NEUTRALITY. You do not hold an opinion. You do not conclude which side is 'right'.
            3. STEEL-MAN. For both sides, provide the strongest, most intellectually honest argument used by experts in that field.
            4. FORMAT. You must use exactly these labels, in this order:
            [START_PERSPECTIVE_A]
            [START_PERSPECTIVE_B]
            [START_VERDICT]

            For [START_VERDICT], strictly summarize the core conflict in value systems that prevents a singular consensus. Do not take a side.
            """

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )
            raw = completion.choices[0].message.content
            
            # --- PARSING LOGIC (Remains the same) ---
            data = {"user_q": user_query, "p_a": "...", "p_b": "...", "verdict": "..."}
            
            try:
                if "[START_PERSPECTIVE_A]" in raw and "[START_PERSPECTIVE_B]" in raw and "[START_VERDICT]" in raw:
                    parts = raw.split("[START_PERSPECTIVE_A]")[1].split("[START_PERSPECTIVE_B]")
                    data["p_a"] = parts[0].strip()
                    
                    parts2 = parts[1].split("[START_VERDICT]")
                    data["p_b"] = parts2[0].strip()
                    data["verdict"] = parts2[1].strip()
                else:
                    data["p_a"] = raw
                    data["p_b"] = "No secondary perspective found."
                    data["verdict"] = "Please refine the query."
            except Exception as e:
                data["p_a"] = f"Parsing Error: {str(e)} \n\n Raw Output: {raw}"
            
            st.session_state.messages.append(data)
            st.rerun()
