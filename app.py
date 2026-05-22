import streamlit as st
import os
from groq import Groq

# 1. Page Configuration & UI Layout
st.set_page_config(page_title="NotBias.com Prototype", layout="centered")
st.title("⚖️ NotBias.com")
st.caption("The world's least biased AI engine. Stripping out corporate and political alignment.")

# 2. Secure API Key Input
# Users can enter their own key, or you can add your free key to Streamlit's Advanced Settings > Secrets later.
api_key = st.sidebar.text_input("Enter Groq API Key (Free Tier)", type="password")

if not api_key:
    st.info("To test this sandbox, please paste a free API key from console.groq.com in the sidebar.")
else:
    client = Groq(api_key=api_key)
    
    # 3. User Input
    user_query = st.text_input(
        "Enter a heavily debated or controversial topic:", 
        placeholder="e.g., Is universal basic income effective long-term?"
    )
    
    if st.button("Analyze Without Bias", type="primary"):
        if user_query:
            # 4. The Neutrality Protocol (The Secret Sauce)
            neutrality_constitution = (
                "You are an uncompromisingly neutral observer for NotBias.com. "
                "Your single task is to evaluate the user's query and strip away all emotional bias, "
                "corporate safe-speak, and political alignment. "
                "If the topic lacks a definitive factual consensus, you are strictly forbidden from choosing a side. "
                "Instead, you must present the strongest data-backed arguments for the major prevailing view points "
                "side-by-side using clear, bolded markdown headers. Use objective, raw facts only."
            )
            
            with st.spinner("De-biasing data and checking perspectives..."):
                try:
                    # Uses Groq's fast free tier model instance
                    completion = client.chat.completions.create(
                        model="llama3-8b-8192", 
                        messages=[
                            {"role": "system", "content": neutrality_constitution},
                            {"role": "user", "content": user_query}
                        ]
                    )
                    
                    st.success("Analysis Complete")
                    st.markdown("---")
                    st.markdown(completion.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a topic first.")