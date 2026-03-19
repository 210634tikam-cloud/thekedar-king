import streamlit as st
import pdfplumber
import pandas as pd
import google.generativeai as genai
import json
import io
import time
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- UI CONFIG ---
st.set_page_config(page_title="Thekedar King Supreme 👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050a18; color: #e0e0e0; }
    .main-header { background: linear-gradient(90deg, #ffd700, #ff8c00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: bold; text-align: center; }
    .calc-display { background: #000; border: 2px solid #ff8c00; padding: 15px; border-radius: 10px; font-family: 'Courier New', monospace; color: #00ff00; text-align: right; font-size: 1.5rem; box-shadow: 0 0 15px #ff8c00; }
    .metric-box { background: #111827; border-left: 5px solid #ff8c00; padding: 10px; margin: 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- AI CORE ENGINE ---
def deep_analyze_tender(pdf_text, api_key, location, target_profit):
    genai.configure(api_key=api_key)
    # UPDATED MODEL NAME HERE
    model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config={"response_mime_type": "application/json"})
    
    prompt = f"""
    Act as the Supreme Construction Auditor for Nepal e-GP. Analyze this BOQ/Tender for {location}.
    Target: 99.99% winning accuracy. Current Profit Goal: {target_profit}%.
    Return JSON ONLY with: project, total_estimate_npr, your_supreme_bid, win_probability, boq_detailed, unbalanced_strategy, red_flags.
    """
    response = model.generate_content(f"{prompt}\n\nPDF TEXT:\n{pdf_text[:50000]}")
    return json.loads(response.text)

# --- DASHBOARD ---
st.markdown("<div class='main-header'>👑 THEKEDAR KING SUPREME</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Control Panel")
    api_key = st.text_input("Gemini API Key", type="password")
    location_filter = st.selectbox("Location", ["Kathmandu", "Pokhara", "Lalitpur", "Chitwan", "Other"])
    profit_margin = st.slider("Profit %", 5, 25, 12)
    st.info("System Status: Ready 2026")

uploaded_files = st.file_uploader("Upload Tender PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 START SUPREME ANALYSIS"):
        if not api_key:
            st.error("Bhai, API Key daalo pehle!")
        else:
            for file in uploaded_files:
                # --- REAL TIME CALCULATION DISPLAY ---
                calc_placeholder = st.empty()
                status_placeholder = st.empty()
                
                with pdfplumber.open(file) as pdf:
                    full_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

                # Fake "Processing" effect for Real-time feel
                for i in range(0, 101, 20):
                    calc_placeholder.markdown(f"""
                    <div class='calc-display'>
                        Scanning BOQ... {i}% <br>
                        Processing Rates... NPR {i*12547:,}
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.3)

                try:
                    data = deep_analyze_tender(full_text, api_key, location_filter, profit_margin)
                    
                    # Final Calc Display
                    calc_placeholder.markdown(f"""
                    <div class='calc-display'>
                        BID TOTAL: NPR {data['your_supreme_bid']:,} <br>
                        CONFIDENCE: {data['win_probability']}%
                    </div>
                    """, unsafe_allow_html=True)

                    st.success(f"Analysis Complete for {file.name}")
                    
                    # Layout Results
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.subheader("📊 Detailed BOQ Breakdown")
                        st.dataframe(pd.DataFrame(data['boq_detailed']), use_container_width=True)
                    
                    with col2:
                        st.markdown("<div class='metric-box'>", unsafe_allow_html=True)
                        st.write("### 🏗️ Strategy")
                        st.write(data['unbalanced_strategy'])
                        st.write("### 🚨 Risks")
                        for r in data['red_flags']:
                            st.error(r)
                        st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.caption("v5.1 | Real-time Calculation Engine Enabled")
