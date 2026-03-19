import streamlit as st
import pdfplumber
import google.generativeai as genai
import json
import time

# --- SIMPLEST STABLE VERSION ---
st.set_page_config(page_title="Thekedar King Final", layout="wide")

st.markdown("<h1 style='text-align: center; color: #ffd700;'>👑 THEKEDAR KING SUPREME</h1>", unsafe_allow_html=True)

api_key = st.sidebar.text_input("🔑 Paste API Key Here", type="password")
uploaded_file = st.file_uploader("📂 Upload BOQ PDF", type="pdf")

if uploaded_file and st.button("⚡ EXECUTE ANALYSIS"):
    if not api_key:
        st.error("Bhai, API Key toh daalo!")
    else:
        try:
            genai.configure(api_key=api_key)
            # Sabse stable model pick kar rahe hain
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

            st.info("Neural Link established... Processing BOQ Data...")
            
            # Simple Prompt to avoid JSON errors
            response = model.generate_content(f"Analyze this Nepal BOQ. Return only a short summary of suggested bid and 3 risks. DATA: {text[:15000]}")
            
            st.success("✅ ANALYSIS COMPLETE")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"🛑 Error: {str(e)}")
            st.info("Check if your API key is correct and has 'Generative Language API' enabled in Google Cloud.")
