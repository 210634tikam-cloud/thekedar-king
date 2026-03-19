import streamlit as st
import pdfplumber
import pandas as pd
import google.generativeai as genai
import json
import time

# --- STABLE UI CONFIG ---
st.set_page_config(page_title="Thekedar King Supreme v6.5", layout="wide")

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

# --- HYBRID INTELLIGENCE ENGINE (ANTI-ERROR) ---
def run_analysis(pdf_text, api_key, region, margin):
    try:
        genai.configure(api_key=api_key)
        
        # 🛡️ ANTI-404 LOGIC: Try all possible models automatically
        model_list = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
        selected_model = None
        
        for m_name in model_list:
            try:
                temp_model = genai.GenerativeModel(m_name)
                # Quick small test call
                temp_model.generate_content("hi", generation_config={"max_output_tokens": 1})
                selected_model = temp_model
                break 
            except:
                continue
        
        if not selected_model:
            return {"error_status": "Google API is rejecting all models. Please check if your API Key is active or billing is enabled."}

        prompt = f"""
        Act as a Nepal Tender Expert. Analyze BOQ for {region} with {margin}% profit.
        Return ONLY a JSON response:
        {{
            "project": "Project Name",
            "your_supreme_bid": 1234567,
            "win_probability": 92,
            "unbalanced_strategy": "Explain strategy",
            "red_flags": ["Risk 1"],
            "boq_table": [{{"item": "Work", "suggested_rate": 100}}]
        }}
        """
        # Limiting text to avoid 413 or Timeout errors
        response = selected_model.generate_content(f"{prompt}\n\nDATA:\n{pdf_text[:20000]}")
        
        # Clean JSON Formatting
        res_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(res_text)
        
    except Exception as e:
        return {"error_status": str(e)}

# --- UI INTERFACE ---
st.markdown("<div class='main-header'>👑 THEKEDAR KING SUPREME</div>", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛰️ System Controls")
    api_key = st.text_input("🔑 API Access Key", type="password")
    location = st.selectbox("🌍 Region", ["Kathmandu", "Lalitpur", "Pokhara", "Nepal-Wide"])
    profit = st.slider("💰 Margin Optimization %", 5, 35, 15)
    st.divider()
    st.info("Engine: Fallback-Enabled v6.5")

uploaded_file = st.file_uploader("📂 Drop Tender PDF", type="pdf")

if uploaded_file and st.button("⚡ EXECUTE NEURAL ANALYSIS"):
    if not api_key:
        st.error("Error: API Key is required to connect to Neural Link.")
    else:
        terminal_msg = st.empty()
        calc_msg = st.empty()
        
        # Extract PDF
        with pdfplumber.open(uploaded_file) as pdf:
            full_text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

        # High-Tech Animation
        logs = ["Bypassing 404 Model Filters...", "Neural Handshake Established...", "Scanning BOQ Nodes...", "Optimizing L1 Rates..."]
        for i, log in enumerate(logs):
            terminal_msg.markdown(f"<div class='terminal-box'>> {log}</div>", unsafe_allow_html=True)
            calc_msg.markdown(f"<div class='calc-screen'><span class='formula-tag'>f(x) = Rate * (1 + {profit/100})</span><br>CALCULATING... {(i+1)*25}%<br>NPR {(i+1)*512400:,}</div>", unsafe_allow_html=True)
            time.sleep(0.6)

        # AI Execution
        result = run_analysis(full_text, api_key, location, profit)

        if "error_status" in result:
            st.error(f"🛑 Error: {result['error_status']}")
            st.info("Tip: If it says 404 again, wait 1 minute and click Execute again. Google is sometimes slow to sync keys.")
        else:
            calc_msg.markdown(f"<div class='calc-screen' style='border-color: #22c55e;'><span style='color:#fbbf24'>FINAL SUPREME BID</span><br>NPR {result.get('your_supreme_bid', 0):,}<br>WIN CHANCE: {result.get('win_probability', 0)}%</div>", unsafe_allow_html=True)
            st.balloons()
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.subheader("🧠 Winning Strategy")
                st.info(result.get('unbalanced_strategy', 'Standard Bidding'))
            with c2:
                st.subheader("🚨 Risk assessment")
                for r in result.get('red_flags', []):
                    st.warning(r)
            
            st.subheader("📊 Itemized Rate Analysis")
            st.table(pd.DataFrame(result.get('boq_table', [])))

st.divider()
st.caption("v6.5 Stable | Proprietary Intelligence for Nepal Construction 2026")
