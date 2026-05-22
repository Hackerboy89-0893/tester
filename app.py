import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="NotBias.com Prototype", layout="centered")
st.title("⚖️ NotBias.com")
st.caption("The world's least biased AI engine. Stripping out corporate and political alignment.")

# 2. Secure API Key Pull
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("API Key missing. Please configure GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

# 3. Modern Chat Input with Built-in Send Button
# This replaces both the text box and the separate button, placing a send arrow right inside the bar!
if user_query := st.chat_input("Enter a heavily debated or controversial topic..."):
    
    # Show the user's question on screen
    st.chat_message("user").markdown(user_query)
    
    # 4. The Neutrality Protocol
    neutrality_constitution = (
        "You are an uncompromisingly neutral observer for NotBias.com. "
        "Your single task is to evaluate the user's query and strip away all emotional bias, "
        "corporate safe-speak, and political alignment. "
        "If the topic lacks a definitive factual consensus, you are strictly forbidden from choosing a side. "
        "Instead, you must present the strongest data-backed arguments for the major prevailing viewpoints "
        "side-by-side using clear, bolded markdown headers. Use objective, raw facts only."
    )
    
    # 5. Generate and Display Response
    with st.chat_message("assistant"):
        with st.spinner("De-biasing data and checking perspectives..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant", 
                    messages=[
                        {"role": "system", "content": neutrality_constitution},
                        {"role": "user", "content": user_query}
                    ]
                )
                st.markdown(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
