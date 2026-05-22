import streamlit as st
from groq import Groq
import uuid

# (Keep your existing Page Config and CSS up to the '.card-data' class)
# ADD THIS TO YOUR CSS SECTION TO STYLE THE NEW VERDICT CARD
st.markdown("""
<style>
    /* ... (Keep previous CSS) ... */
    .card-verdict { border-top: 4px solid #a855f7; background: #faf5ff; }
</style>
""", unsafe_allow_html=True)

# ... (Keep session state and sidebar code as is) ...

# UPDATE THE PROMPT CONSTITUTION TO INCLUDE THE VERDICT TAG
    tag_constitution = (
        "You are an uncompromisingly neutral observer for NotBias.com.\n\n"
        "Analyze the user's prompt and split your response into exactly four sections "
        "separated by these exact uppercase system tags:\n"
        "[START_PERSPECTIVE_A]\n"
        "[START_PERSPECTIVE_B]\n"
        "[START_BASELINE]\n"
        "[START_VERDICT]\n\n"
        "CRITICAL ARCHITECTURE RULES:\n"
        "1. Perspective A/B: Punchy micro-bullets with **Bold Anchors**.\n"
        "2. Baseline: Raw objective facts.\n"
        "3. Verdict: A concise 2-sentence synthesis of why this is debated and the objective middle ground."
    )

# ... (Keep your chat loop until the Assistant rendering logic) ...

    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner("Isolating spectrum markers..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": tag_constitution},
                        {"role": "user", "content": user_query}
                    ]
                )
                
                raw_text = completion.choices[0].message.content
                
                # ADAPTIVE PARSING ENGINE (Updated for 4 tags)
                p_a, p_b, baseline, verdict = "...", "...", "...", "..."
                
                if "[START_PERSPECTIVE_A]" in raw_text:
                    remainder_a = raw_text.split("[START_PERSPECTIVE_A]", 1)[1]
                else: remainder_a = raw_text

                if "[START_PERSPECTIVE_B]" in remainder_a:
                    p_a, remainder_b = remainder_a.split("[START_PERSPECTIVE_B]", 1)
                else: p_a, remainder_b = remainder_a, ""

                if "[START_BASELINE]" in remainder_b:
                    p_b, remainder_c = remainder_b.split("[START_BASELINE]", 1)
                else: p_b, remainder_c = remainder_b, ""

                if "[START_VERDICT]" in remainder_c:
                    baseline, verdict = remainder_c.split("[START_VERDICT]", 1)
                else: baseline = remainder_c
                
                # RENDER UI
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="ui-card card-left"><div class="card-header">🟢 Perspective A</div></div>', unsafe_allow_html=True)
                    st.markdown(p_a.strip())
                with col2:
                    st.markdown('<div class="ui-card card-right"><div class="card-header">🔵 Perspective B</div></div>', unsafe_allow_html=True)
                    st.markdown(p_b.strip())
                
                st.markdown('<div class="ui-card card-data"><div class="card-header">📊 Metrics</div></div>', unsafe_allow_html=True)
                st.markdown(baseline.strip())
                
                # NEW FINAL VERDICT CARD
                st.markdown(f'<div class="ui-card card-verdict"><div class="card-header">⚖️ Final Verdict</div>{verdict.strip()}</div>', unsafe_allow_html=True)
                
                # Save to history
                current_session["messages"].append({"role": "assistant", "p_a": p_a, "p_b": p_b, "baseline": baseline, "verdict": verdict})
                st.rerun()
            except Exception as e:
                st.error(f"Core Error: {e}")
