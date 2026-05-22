import streamlit as st
import json
from groq import Groq

# 1. Expand layout and set page config
st.set_page_config(page_title="NotBias.com", layout="wide")

# 2. Inject Premium Custom CSS UI Theme
st.markdown("""
<style>
    /* Global Font & Spacing tweaks */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [data-testid="stMarkdownContainer"] {
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    /* Custom CSS Card Component Design */
    .ui-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #eef1f6;
        margin-bottom: 20px;
    }
    .card-left { border-top: 4px solid #10b981; }  /* Green accent */
    .card-right { border-top: 4px solid #3b82f6; } /* Blue accent */
    .card-data { border-left: 4px solid #6b7280; background-color: #f8fafc; } /* Gray baseline */
    
    .card-header {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

# App branding layout
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
    
    # Updated constitution that strictly outlaws dense text walls
    json_constitution = (
        "You are a neutral backend data processor for NotBias.com. "
        "Analyze the user's prompt and output a valid JSON object with exactly three keys: "
        "'left_perspective', 'right_perspective', and 'statistical_baseline'.\n\n"
        
        "CRITICAL VISUAL FORMATTING RULES:\n"
        "1. NEVER write heavy paragraphs or multi-sentence blocks of text.\n"
        "2. Break all information down into short, highly scannable micro-bullet points (max 12 words per bullet).\n"
        "3. Every single bullet point MUST start with a **Bold Key Phrase** action-anchor followed by a short explanation.\n"
        "4. Use a clean line break between bullet points to ensure high breathing room.\n\n"
        
        "- 'left_perspective': Highly polished, steel-manned arguments from the progressive/interventionist angle structured as short bolded bullets.\n"
        "- 'right_perspective': Highly polished, steel-manned arguments from the conservative/free-market angle structured as short bolded bullets.\n"
        "- 'statistical_baseline': Pure, unarguable data parameters, cold facts, or undisputed structural timelines related to the topic.\n\n"
        "Do not include any text outside the JSON brackets."
    )
    
    with st.chat_message("assistant"):
        with st.spinner("Isolating viewpoints..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": json_constitution},
                        {"role": "user", "content": user_query}
                    ],
                    response_format={"type": "json_object"} 
                )
                
                data = json.loads(completion.choices[0].message.content)
                
                # Visual Side-by-Side Card Layout
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="ui-card card-left">
                        <div class="card-header">🟢 Perspective A</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(data.get("left_perspective", "Data missing."))
                    
                with col2:
                    st.markdown(f"""
                    <div class="ui-card card-right">
                        <div class="card-header">🔵 Perspective B</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(data.get("right_perspective", "Data missing."))
                    
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Baseline Facts Card
                st.markdown(f"""
                <div class="ui-card card-data">
                    <div class="card-header">📊 Objective Baseline Metrics</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(data.get("statistical_baseline", "Data missing."))
                
            except Exception as e:
                st.error(f"Error compiling dashboard: {e}")
