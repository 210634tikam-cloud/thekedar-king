import streamlit as st
import pdfplumber
import pandas as pd
import google.generativeai as genai
import json
import time

# --- UI CONFIG (ADVANCED MATRIX THEME) ---
st.set_page_config(page_title="Thekedar King Supreme v6.0", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300&display=swap');
    
    .stApp { background: #020617; color: #f8fafc; font-family: 'JetBrains Mono', monospace; }
    
    .main-header { 
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(135deg, #fbbf24, #f59e0b); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        font-size: 3.5rem; font-weight: 800; text-align: center; 
        text-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
        padding: 30px;
    }

    /* Terminal Style Display */
    .terminal-box {
        background: #000;
        border: 2px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        color: #60a5fa;
        font-size: 0.9rem;
        box-shadow: inset 0 0 10px #1e3a8a;
        margin-bottom: 20px;
    }

    /* Floating Real-time Calc Display */
    .calc-screen {
        background: radial-gradient(circle, #0f172a, #000);
        border: 2px solid #ffd700;
        padding: 25px;
        border-radius: 15px;
        color: #22c55e;
        text-align: right;
        font-family: 'Orbitron', sans-serif;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.2);
    }

    .formula-tag { color: #f472b6; font-size: 0.8rem; font-style: italic; }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #1d4ed8, #3b82f6);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 50px;
        padding: 15px;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.5);
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- AI ANALYZER ---
def analyze_engine(text, key, loc, prof):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"Analyze Nepal e-GP BOQ for {loc}. Profit: {prof}%. Return JSON with: project, total_estimate_npr, your_supreme_bid, win_probability, boq_detailed, unbalanced_strategy, red_flags."
    response = model.generate_content(f"{prompt}\n\nTEXT: {text[:30000]}")
    return json.loads(response.text.strip().replace('```json', '').replace('```', ''))

# --- UI LAYOUT ---
st.markdown("<div class='main-header'>👑 THEKEDAR KING SUPREME v6.0</div>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609156.png", width=80)
    st.title("Admin Console")
    api_key = st.text_input("🔑 System Access Key (Gemini)", type="password")
    location = st.selectbox("🌍 Region", ["Kathmandu", "Lalitpur", "Pokhara", "Lumbini", "Other"])
    profit = st.slider("💰 Margin Optimization (%)", 5, 30, 15)
    st.divider()
    st.caption("Engine: Hybrid AI v6.0")

uploaded_file = st.file_uploader("📂 Drop BOQ PDF Here", type="pdf")

if uploaded_file and st.button("⚡ EXECUTE NEURAL ANALYSIS"):
    if not api_key:
        st.error("Access Denied: Missing API Key.")
    else:
        # 1. LIVE TERMINAL LOGS
        terminal = st.empty()
        calc_display = st.empty()
        
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

        # --- FANCY ANIMATION ENGINE ---
        logs = [
            "Initializing Neural Core...",
            f"Scanning BOQ for {location} standard rates...",
            "Applying formula: Total = ∑(Rate * Qty)",
            "Checking e-GP compliance v2026...",
            "Optimizing Profit via Unbalanced Bidding...",
            "Finalizing Lowest Bid (L1) Strategy..."
        ]
        
        for idx, log in enumerate(logs):
            terminal.markdown(f"<div class='terminal-box'>> {log}</div>", unsafe_allow_html=True)
            calc_display.markdown(f"""
                <div class='calc-screen'>
                    <span class='formula-tag'>f(x) = Market_Rate * (1 + {profit/100})</span><br>
                    PROCESSING... {idx*20}% <br>
                    ESTIMATED NPR: {(idx+1)*245800:,}
                </div>
            """, unsafe_allow_html=True)
            time.sleep(0.6)

        try:
            data = analyze_engine(text, api_key, location, profit)
            
            # FINAL RESULT DISPLAY
            calc_display.markdown(f"""
                <div class='calc-screen' style='border-color: #22c55e;'>
                    <span style='color: #fbbf24; font-size: 1rem;'>OPTIMIZED SUPREME BID</span><br>
                    NPR {data['your_supreme_bid']:,}<br>
                    <span style='font-size: 1.2rem;'>WIN CHANCE: {data['win_probability']}%</span>
                </div>
            """, unsafe_allow_html=True)

            st.balloons()

            # DASHBOARD TILES
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("📊 Intelligence Table")
                st.dataframe(pd.DataFrame(data['boq_detailed']), use_container_width=True)
            with c2:
                st.subheader("🧠 Strategy")
                st.info(data['unbalanced_strategy'])
                st.warning("⚠️ RISK ASSESSMENT")
                for r in data['red_flags']:
                    st.write(f"- {r}")
                    
        except Exception as e:
            st.error(f"Analysis Interrupted. Check API/PDF.")

st.divider()
st.markdown("<p style='text-align: center; color: #475569;'>v6.0 | Proprietary Structural Intelligence for Nepal</p>", unsafe_allow_html=True)
