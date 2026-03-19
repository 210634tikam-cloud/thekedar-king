import streamlit as st
import pdfplumber
import pandas as pd
import google.generativeai as genai
import json
import time

# --- UI CONFIG (NEPAL 2026 EDITION) ---
st.set_page_config(page_title="Thekedar King Supreme 👑", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #050a18; color: #e0e0e0; }
    .main-header { 
        background: linear-gradient(90deg, #ffd700, #ff8c00); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 3rem; 
        font-weight: bold; 
        text-align: center; 
        padding: 20px;
    }
    .calc-display { 
        background: #000; 
        border: 2px solid #ff8c00; 
        padding: 20px; 
        border-radius: 12px; 
        font-family: 'Courier New', monospace; 
        color: #00ff00; 
        text-align: right; 
        font-size: 1.8rem; 
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.5);
        margin-bottom: 20px;
    }
    .metric-card { 
        background: #111827; 
        border-radius: 10px; 
        padding: 15px; 
        border-left: 5px solid #ffd700;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AI ENGINE (STABLE PRO MODEL) ---
def deep_analyze_tender(pdf_text, api_key, location, target_profit):
    genai.configure(api_key=api_key)
    # Using 'gemini-1.5-pro' for maximum stability and depth
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Act as the Supreme Construction Auditor for Nepal e-GP (2026). Analyze this BOQ/Tender for {location}.
    Target: 99.99% winning accuracy. Current Profit Goal: {target_profit}%.
    
    Return ONLY a JSON object with these keys:
    "project": "Project Name",
    "total_estimate_npr": 5000000,
    "your_supreme_bid": 4850000,
    "win_probability": 95,
    "boq_detailed": [{"item": "Excavation", "market_rate": 500, "suggested_rate": 550}],
    "unbalanced_strategy": "Explain front-loading here",
    "red_flags": ["Risk 1", "Risk 2"]
    """
    
    response = model.generate_content(f"{prompt}\n\nPDF CONTENT:\n{pdf_text[:40000]}")
    # Cleaning response to ensure only JSON is parsed
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)

# --- DASHBOARD UI ---
st.markdown("<div class='main-header'>👑 THEKEDAR KING SUPREME</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Control Tower")
    api_key = st.text_input("Gemini API Key", value="", type="password", help="Enter your AIza... key here")
    location_filter = st.selectbox("Project Location", ["Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara", "Chitwan", "Butwal", "Other"])
    profit_margin = st.slider("Target Profit Margin %", 5, 25, 12)
    st.divider()
    st.success("System: Online (Nepal 2026)")

# File Upload Section
uploaded_file = st.file_uploader("Upload BOQ or Tender PDF", type="pdf")

if uploaded_file:
    if st.button("🚀 START SUPREME ANALYSIS"):
        if not api_key:
            st.error("Bhai, pehle Sidebar mein API Key toh daalo!")
        else:
            # Placeholders for real-time feel
            calc_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            with pdfplumber.open(uploaded_file) as pdf:
                full_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

            # --- DIGITAL CALCULATION DISPLAY (LIVE EFFECT) ---
            for i in range(1, 101, 10):
                calc_placeholder.markdown(f"""
                <div class='calc-display'>
                    SCANNING BOQ... {i}% <br>
                    EXTRACTING RATES... NPR {i * 15840:,}
                </div>
                """, unsafe_allow_html=True)
                progress_bar.progress(i)
                time.sleep(0.2)

            try:
                # Actual AI Call
                data = deep_analyze_tender(full_text, api_key, location_filter, profit_margin)
                
                # Final Display Update
                calc_placeholder.markdown(f"""
                <div class='calc-display' style='color: #ffd700;'>
                    FINAL BID: NPR {data['your_supreme_bid']:,} <br>
                    WIN CHANCE: {data['win_probability']}%
                </div>
                """, unsafe_allow_html=True)

                st.balloons()

                # Results Layout
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📊 Strategic BOQ Analysis")
                    df = pd.DataFrame(data['boq_detailed'])
                    st.table(df) # Using table for better mobile view
                
                with col2:
                    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                    st.write("### 🏗️ Unbalanced Strategy")
                    st.info(data['unbalanced_strategy'])
                    
                    st.write("### 🚨 Critical Risks (Red Flags)")
                    for flag in data['red_flags']:
                        st.error(flag)
                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"System Error: {str(e)}")
                st.info("Tip: Make sure your API key is correct and you have internet.")

st.divider()
st.caption("v5.2 Stable | Proprietary Intelligence for Nepal Construction Industry 2026")
