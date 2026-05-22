import streamlit as st
from groq import Groq
import uuid

st.set_page_config(page_title="NotBias", layout="centered")

st.markdown("""
<style>
    /* Purple Theme & Minimalism */
    :root { --accent: #7c3aed; }
    .stApp { background-color: #f8fafc; }
    
    /* Hero Headline */
    .hero-container { padding: 40px 0; text-align: left; }
    .hero-h1 { font-size: 64px; font-weight: 800; line-height: 1.1; margin-bottom: 20px; }
    .hero-h1 span { color: #7c3aed; }
    .hero-sub { font-size: 18px; color: #6b7280; margin-bottom: 30px; line-height: 1.6; }
    
    /* Input/CTA */
    .stChatInput { padding-top: 20px; }
    div[data-testid="stChatInput"] { border-radius: 12px; border: 1px solid #e5e7eb; }
    
    /* Stats Row */
    .stats-row { display: flex; gap: 30px; margin-top: 20px; font-family: monospace; font-size: 12px; color: #94a3b8; }
    
    /* Cards */
    .ui-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; margin-top: 10px; }
    .card-left { border-left: 4px solid #10b981; }
    .card-right { border-left: 4px solid #3b82f6; }
    .card-verdict { border-left: 4px solid #7c3aed; background: #faf5ff; }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-h1">The AI that gives you <span>every side</span> of the story.</div>
    <p class="hero-sub">Ask any contested question. Get the strongest case for every credible position — sourced, reasoned, and completely agenda-free.</p>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div class="stats-row">
    <span>0 OPINIONS HELD</span>
    <span>2+ SIDES PER ANSWER</span>
    <span>100% SOURCE-CITED</span>
</div>
""", unsafe_allow_html=True)

# Main Interaction Area
if user_query := st.chat_input("Ask a question..."):
    # ... (Keep your existing Groq logic here)
    st.rerun()

# Display logic stays the same but uses the new .ui-card classes
