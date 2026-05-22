import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="NotBias.com Prototype", layout="centered")
st.title("⚖️ NotBias.com")

# Pull the secret securely from Streamlit's backend (hidden from the public)
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("API Key missing. Please configure GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

user_query = st.text_input("Enter a heavily debated or controversial topic:")

# ... the rest of your button and layout code remains exactly the same!
