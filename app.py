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
    
    # THE FIX: Explicitly commanding flat strings to satisfy Groq's JSON validator
    json_constitution = (
        "You are a neutral backend data processor for NotBias.com. "
        "You must analyze the user's prompt and output a valid JSON object with exactly three keys: "
        "'left_perspective', 'right_perspective', and 'statistical_baseline'.\n\n"
        "CRITICAL CODE RULES:\n"
        "1. The value for EVERY key MUST be a flat plain text string.\n"
        "2. Do NOT create nested dictionary objects, arrays, or lists inside the values.\n"
        "3. If you want to list items, format them as a single string using standard text-based bullet points or line breaks.\n\n"
        "- 'left_perspective': A comprehensive text string explaining the arguments from the progressive, reformist, or interventionist side.\n"
        "- 'right_perspective': A comprehensive text string explaining the arguments from the conservative, traditional, or free-market side.\n"
        "- 'statistical_baseline': A text string listing raw, unarguable data points, historical facts, or baseline metrics related to the topic, completely stripped of all opinion.\n\n"
        "Do not include any text outside the JSON object brackets."
    )
    
    with st.chat_message("assistant"):
        with st.spinner("Isolating viewpoints..."):
            try:
                # Call Groq using JSON Mode
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": json_constitution},
                        {"role": "user", "content": user_query}
                    ],
                    response_format={"type": "json_object"} 
                )
                
                # Parse the JSON response
                data = json.loads(completion.choices[0].message.content)
                
                # Create the Visual Split Screen Layout
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
