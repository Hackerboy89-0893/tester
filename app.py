import streamlit as st
from groq import Groq

# 1. Expand layout and set page config
st.set_page_config(page_title="NotBias.com", layout="wide")

# Inject Premium Custom CSS UI Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [data-testid="stMarkdownContainer"] {
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    .ui-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #eef1f6;
        margin-bottom: 20px;
    }
    .card-left { border-top: 4px solid #10b981; }  
    .card-right { border-top: 4px solid #3b82f6; } 
    .card-data { border-left: 4px solid #6b7280; background-color: #f8fafc; } 
    
    .card-header {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚖️ NotBias.com")
st.caption("Engineered machine neutrality through multi-perspective isolation.")

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("API Key missing in Secrets.")
    st.stop()

if user_query := st.chat_input("Enter a heavily debated or controversial topic..."):
    st.chat_message("user").markdown(user_query)
    
    # SYSTEM PROMPT: Uses plain text markers instead of high-risk JSON structures
    tag_constitution = (
        "You are an uncompromisingly neutral observer for NotBias.com.\n\n"
        "Analyze the user's prompt and split your response into exactly three sections. "
        "You MUST separate the sections using these exact text dividers uppercase tags:\n"
        "[START_PERSPECTIVE_A]\n"
        "[START_PERSPECTIVE_B]\n"
        "[START_BASELINE]\n\n"
        "CRITICAL FORMATTING RULES:\n"
        "1. Never write heavy walls of text. Break information into highly scannable bullet points.\n"
        "2. Every bullet point must start with a **Bold Key Phrase Anchor** followed by a short explanation.\n"
        "3. Provide equal depth, real estate, and structural tone to both Perspectives.\n\n"
        "Structure your entire output exactly like this:\n"
        "[START_PERSPECTIVE_A]\n"
        "* **Anchor Keyword:** Detail point here.\n"
        "* **Anchor Keyword:** Detail point here.\n"
        "[START_PERSPECTIVE_B]\n"
        "* **Anchor Keyword:** Detail point here.\n"
        "* **Anchor Keyword:** Detail point here.\n"
        "[START_BASELINE]\n"
        "* **Metric:** Raw objective factual data points here."
    )
    
    with st.chat_message("assistant"):
        with st.spinner("Isolating viewpoints..."):
            try:
                # Call Groq without the rigid JSON mode constraint
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": tag_constitution},
                        {"role": "user", "content": user_query}
                    ]
                )
                
                raw_text = completion.choices[0].message.content
                
                # Robust Safe-Parsing Fallback Logic
                p_a, p_b, baseline = "Data extraction failed.", "Data extraction failed.", "Data extraction failed."
                
                if "[START_PERSPECTIVE_A]" in raw_text and "[START_PERSPECTIVE_B]" in raw_text and "[START_BASELINE]" in raw_text:
                    try:
                        part_a_and_more = raw_text.split("[START_PERSPECTIVE_A]")[1]
                        p_a, remaining = part_a_and_more.split("[START_PERSPECTIVE_B]")
                        p_b, baseline = remaining.split("[START_BASELINE]")
                        p_a, p_b, baseline = p_a.strip(), p_b.strip(), baseline.strip()
                    except Exception:
                        # Fallback if text splitting clips weirdly
                        p_a, p_b, baseline = raw_text, "Review full transcript below.", ""
                else:
                    p_a = raw_text
                
                # Render UI Columns using parsed text
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A</div></div>', unsafe_allow_html=True)
                    st.markdown(p_a)
                    
                with col2:
                    st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B</div></div>', unsafe_allow_html=True)
                    st.markdown(p_b)
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Objective Baseline Metrics</div></div>', unsafe_allow_html=True)
                st.markdown(baseline)
                
            except Exception as e:
                st.error(f"Error compiling dashboard: {e}")
