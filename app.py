import streamlit as st
import json
from groq import Groq

st.set_page_config(page_title="NotBias.com", layout="wide") # Set to wide layout for columns
st.title("⚖️ NotBias.com")
st.caption("Forcing machine neutrality through multi-perspective isolation.")

try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("API Key missing in Secrets.")
    st.stop()

if user_query := st.chat_input("Enter a heavily debated or controversial topic..."):
    st.chat_message("user").markdown(user_query)
    
    # 1. System Prompt instructing JSON output
    json_constitution = (
        "You are a neutral backend data processor for NotBias.com. "
        "You must analyze the user's prompt and output a JSON object with exactly three keys: "
        "'left_perspective', 'right_perspective', and 'statistical_baseline'.\n\n"
        "- 'left_perspective': The strongest, most steel-manned arguments from the progressive, reformist, or interventionist side.\n"
        "- 'right_perspective': The strongest, most steel-manned arguments from the conservative, traditional, or free-market side.\n"
        "- 'statistical_baseline': Pure, unarguable data points, historical facts, or economic baselines related to the topic, stripped of all adjectives.\n\n"
        "Do not include any text outside the JSON object."
    )
    
    with st.chat_message("assistant"):
        with st.spinner("Isolating viewpoints..."):
            try:
                # 2. Call Groq using JSON Mode
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": json_constitution},
                        {"role": "user", "content": user_query}
                    ],
                    response_format={"type": "json_object"} # Forces the AI to output perfect JSON
                )
                
                # 3. Parse the JSON response
                data = json.loads(completion.choices[0].message.content)
                
                # 4. Create the Visual Split Screen Layout
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🟢 Perspective A")
                    st.info(data.get("left_perspective", "Data missing."))
                    
                with col2:
                    st.subheader("🔵 Perspective B")
                    st.info(data.get("right_perspective", "Data missing."))
                    
                st.markdown("---")
                st.subheader("📊 Objective Data Baseline")
                st.success(data.get("statistical_baseline", "Data missing."))
                
            except Exception as e:
                st.error(f"Error compiling perspectives: {e}")
