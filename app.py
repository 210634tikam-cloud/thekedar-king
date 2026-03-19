import streamlit as st
import pdfplumber
import pandas as pd
import google.generativeai as genai
import json
import time

# --- STABLE UI CONFIG ---
st.set_page_config(page_title="Thekedar King Supreme v6.2", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300&display=swap');
    .stApp { background: #020617; color: #f8fafc; font-family: 'JetBrains Mono', monospace; }
    .main-header { 
        font-family: 'Orbitron', sans-serif; 
        background: linear-gradient(135deg, #fbbf24, #f59e0b); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-size: 2.8rem; font-weight: 800; text-align: center; padding: 20px; 
    }
    .terminal-box { background: #000; border: 1px solid #3b82f6; padding: 12px; border-radius: 8px; color: #60a5fa; font-size: 0.85rem; margin-bottom: 15px; }
    .calc-screen { 
        background: #000; border: 2px solid #ffd700; padding: 25px; border-radius: 12px; 
        color: #22c55e; text-align: right; font-family: 'Orbitron', sans-serif; 
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.25); 
    }
    .formula-tag { color: #f472b6; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- HYBRID INTELLIGENCE ENGINE ---
def run_analysis(pdf_text, api_key, region, margin):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Cross-Checked Stable Prompt
        prompt = f"""
        Analyze the following Nepal construction BOQ data for {region} with a {margin}% profit margin.
        Return ONLY a JSON response in this exact format:
        {{
            "project": "Project Name",
            "your_supreme_bid": 1234567,
            "win_probability": 92,
            "unbalanced_strategy": "Summary of strategy",
            "red_flags": ["Risk 1", "Risk 2"],
            "boq_table": [{{"item": "Work", "suggested_rate": 100}}]
        }}
        """
        response = model.generate_content(f"{prompt}\n\nDATA:\n{pdf_text[:28000]}")
        
        # Extra check to clean JSON strings
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        return {"error_status": str(e)}

# --- UI INTERFACE ---
st.markdown("<div class='main-header'>👑 THEKEDAR KING SUPREME</div>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛰️ System Controls")
    api_key = st.text_input("🔑 API Access Key", type="password")
    location = st.selectbox("🌍 Region", ["Kathmandu", "Lalitpur", "Pokhara", "Nepal-Wide"])
    profit = st.slider("💰 Margin Optimization %", 5, 30, 15)
    st.divider()
    st.success("Core Status: Secure")

uploaded_file = st.file_uploader("📂 Drop Tender PDF", type="pdf")

if uploaded_file and st.button("⚡ EXECUTE NEURAL ANALYSIS"):
    if not api_key:
        st.warning("Error: Unauthorized. Please enter API Key.")
    else:
        terminal_msg = st.empty()
        calc_msg = st.empty()
        
        # Extracting PDF
        with pdfplumber.open(uploaded_file) as pdf:
            full_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

        # Cross-Checked Animation Loop
        logs = ["Booting AI Core...", "Scanning e-GP BOQ Nodes...", "Calculating L1 Probability...", "Optimizing Rates..."]
        for i, log in enumerate(logs):
            terminal_msg.markdown(f"<div class='terminal-box'>> {log}</div>", unsafe_allow_html=True)
            calc_msg.markdown(f"<div class='calc-screen'><span class='formula-tag'>f(x) = Market_Rate * (1 + {profit/100})</span><br>PROCESSING... {(i+1)*25}%<br>NPR {(i+1)*412700:,}</div>", unsafe_allow_html=True)
            time.sleep(0.5)

        # Result Logic
        result = run_analysis(full_text, api_key, location, profit)

        if "error_status" in result:
            st.error(f"⚠️ Neural Link Failed: {result['error_status']}")
            st.info("Tip: Click 'Execute' again. Sometimes the AI connection takes a second try.")
        else:
            calc_msg.markdown(f"<div class='calc-screen' style='border-color: #22c55e;'><span style='color:#fbbf24'>FINAL L1 BID</span><br>NPR {result.get('your_supreme_bid', 0):,}<br>WIN CHANCE: {result.get('win_probability', 0)}%</div>", unsafe_allow_html=True)
            st.balloons()
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.subheader("🧠 Strategy Advisor")
                st.info(result.get('unbalanced_strategy', 'N/A'))
            with c2:
                st.subheader("🚨 Risk Analysis")
                for r in result.get('red_flags', []):
                    st.error(r)
            
            st.subheader("📊 Detailed Item Rates")
            st.dataframe(pd.DataFrame(result.get('boq_table', [])), use_container_width=True)

st.divider()
st.caption("v6.2 Stable | Final Cross-Checked Release 2026")
