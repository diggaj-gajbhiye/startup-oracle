import streamlit as st
import requests
import json
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="StartupOracle",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─── CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

  :root {
    --bg: #0a0a0f;
    --bg2: #0f0f1a;
    --bg3: #14142a;
    --accent: #7c3aed;
    --accent2: #a855f7;
    --accent3: #c084fc;
    --gold: #f59e0b;
    --text: #f1f0ff;
    --text-secondary: #b4afd6;
    --muted: #8b85a1;
    --border: rgba(124,58,237,0.25);
    --input-bg: #1a1a2e;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
  }
  
  [data-testid="stHeader"], [data-testid="stToolbar"] { 
    display: none !important; 
  }
  
  .main .block-container { 
    padding: 0 !important; 
    max-width: 100% !important; 
  }

  /* ========== FIXED HERO SECTION - PROPER CENTERING ========== */
  .hero {
    text-align: center;
    padding: 52px 20px 36px;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
  }
  
  .hero::before {
    content: ''; 
    position: absolute; 
    top: -80px; 
    left: 50%; 
    transform: translateX(-50%);
    width: 600px; 
    height: 360px;
    background: radial-gradient(ellipse, rgba(124,58,237,0.16) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }
  
  .hero-badge {
    display: inline-block; 
    background: rgba(124,58,237,0.15); 
    border: 1px solid var(--border);
    color: var(--accent3); 
    font-family: 'Space Mono', monospace; 
    font-size: 10px;
    letter-spacing: 3px; 
    text-transform: uppercase; 
    padding: 6px 18px;
    border-radius: 20px; 
    margin-bottom: 20px;
    position: relative;
    z-index: 1;
  }
  
  .hero-title {
    font-family: 'Syne', sans-serif !important; 
    font-size: clamp(2.4rem, 5vw, 4.2rem) !important;
    font-weight: 800 !important; 
    line-height: 1.08 !important; 
    color: var(--text) !important;
    letter-spacing: -2px; 
    margin-bottom: 14px !important;
    text-align: center !important;
    position: relative;
    z-index: 1;
    max-width: 900px;
    margin-left: auto !important;
    margin-right: auto !important;
  }
  
  .hero-title span {
    background: linear-gradient(135deg, var(--accent2), var(--gold));
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  .hero-sub { 
    color: var(--muted); 
    font-size: 1rem; 
    font-weight: 300; 
    max-width: 600px; 
    margin: 0 auto !important;
    line-height: 1.7;
    text-align: center !important;
    position: relative;
    z-index: 1;
    padding: 0 20px;
  }

  .form-wrapper { 
    max-width: 820px; 
    margin: 0 auto; 
    padding: 0 24px 60px; 
  }

  .step-header {
    display: flex; 
    align-items: center; 
    gap: 14px; 
    margin: 32px 0 16px;
    padding: 14px 20px; 
    background: rgba(124,58,237,0.08);
    border: 1px solid var(--border); 
    border-radius: 14px;
  }
  
  .step-num {
    background: linear-gradient(135deg, var(--accent), var(--accent2)); 
    color: white;
    font-family: 'Syne', sans-serif; 
    font-weight: 800; 
    font-size: 0.9rem;
    width: 32px; 
    height: 32px; 
    border-radius: 50%;
    display: flex; 
    align-items: center; 
    justify-content: center; 
    flex-shrink: 0;
  }
  
  .step-title { 
    font-family: 'Syne', sans-serif; 
    font-size: 1rem; 
    font-weight: 700; 
    color: var(--text); 
  }
  
  .step-desc { 
    font-size: 0.8rem; 
    color: var(--muted); 
    margin-top: 2px; 
  }

  /* Input Styles */
  [data-testid="stTextInput"] label,
  [data-testid="stTextArea"] label,
  [data-testid="stSelectbox"] label {
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    margin-bottom: 6px !important;
  }

  [data-testid="stTextInput"] input {
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
  }
  
  [data-testid="stTextInput"] input::placeholder {
    color: var(--muted) !important;
    opacity: 0.7 !important;
    font-weight: 400 !important;
  }
  
  [data-testid="stTextInput"] input:focus {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.12) !important;
    background: var(--bg3) !important;
  }

  [data-testid="stTextArea"] textarea {
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
  }
  
  [data-testid="stTextArea"] textarea::placeholder {
    color: var(--muted) !important;
    opacity: 0.7 !important;
    font-weight: 400 !important;
  }
  
  [data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent2) !important;
    box-shadow: 0 0 0 3px rgba(168,85,247,0.12) !important;
    background: var(--bg3) !important;
  }

  /* Selectbox Styles */
  [data-testid="stSelectbox"] {
    margin-bottom: 16px !important;
  }
  
  [data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    min-height: 44px !important;
  }
  
  [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover {
    border-color: var(--accent2) !important;
    background: var(--bg3) !important;
  }
  
  [data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: var(--text) !important;
    font-size: 0.92rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
  }
  
  [data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] span {
    color: var(--muted) !important;
    opacity: 0.8 !important;
    font-weight: 400 !important;
  }
  
  div[data-baseweb="popover"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
  }
  
  div[data-baseweb="popover"] ul {
    background: var(--bg3) !important;
    padding: 6px 0 !important;
  }
  
  div[data-baseweb="popover"] li {
    background: var(--bg3) !important;
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 10px 16px !important;
    transition: all 0.15s ease !important;
  }
  
  div[data-baseweb="popover"] li:hover {
    background: rgba(124, 58, 237, 0.2) !important;
    color: var(--text) !important;
  }
  
  div[data-baseweb="popover"] li[aria-selected="true"] {
    background: rgba(124, 58, 237, 0.3) !important;
    color: var(--accent3) !important;
    font-weight: 500 !important;
  }
  
  [data-baseweb="select"] svg {
    stroke: var(--accent3) !important;
    fill: var(--accent3) !important;
  }

  /* Button Styles */
  [data-testid="stButton"] button {
    width: 100%; 
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: white !important; 
    border: none !important; 
    border-radius: 14px !important;
    padding: 18px 40px !important; 
    font-family: 'Syne', sans-serif !important;
    font-size: 1.1rem !important; 
    font-weight: 700 !important;
    box-shadow: 0 8px 32px rgba(124,58,237,0.35) !important; 
    margin-top: 24px !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
  }
  
  [data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(124,58,237,0.45) !important;
  }
  
  [data-testid="stButton"] button:active {
    transform: translateY(0) !important;
  }

  /* Result Cards */
  .result-card {
    background: linear-gradient(135deg, rgba(15,15,26,0.95), rgba(20,20,42,0.98));
    border: 1px solid var(--border); 
    border-radius: 20px;
    padding: 32px; 
    margin-top: 24px; 
    position: relative; 
    overflow: hidden;
    backdrop-filter: blur(10px);
  }
  
  .result-card::before {
    content: ''; 
    position: absolute; 
    top: 0; 
    left: 0; 
    right: 0; 
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--gold));
  }
  
  .verdict-badge {
    display: inline-flex; 
    align-items: center; 
    gap: 10px; 
    padding: 10px 24px;
    border-radius: 100px; 
    font-family: 'Syne', sans-serif; 
    font-size: 1.05rem;
    font-weight: 700; 
    margin-bottom: 16px;
  }
  
  .verdict-success { 
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.4);
    color: #34d399; 
  }
  
  .verdict-fail { 
    background: rgba(239,68,68,0.12); 
    border: 1px solid rgba(239,68,68,0.35); 
    color: #f87171; 
  }
  
  .verdict-mixed { 
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.35);
    color: #fbbf24; 
  }

  .metric-grid { 
    display: grid; 
    grid-template-columns: repeat(3,1fr); 
    gap: 14px; 
    margin-top: 18px; 
  }
  
  .metric-box { 
    background: rgba(124,58,237,0.08);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    transition: all 0.2s ease;
  }
  
  .metric-box:hover {
    border-color: rgba(124,58,237,0.5);
    background: rgba(124,58,237,0.12);
  }
  
  .metric-val { 
    font-family: 'Space Mono', monospace; 
    font-size: 1.6rem; 
    font-weight: 700; 
  }
  
  .metric-key { 
    font-size: 0.68rem; 
    color: var(--muted); 
    letter-spacing: 1.5px; 
    text-transform: uppercase; 
    margin-top: 4px; 
  }
  
  .divider { 
    height: 1px; 
    background: var(--border); 
    margin: 20px 0; 
  }
  
  .analysis-title { 
    font-family: 'Syne', sans-serif; 
    font-size: 0.82rem; 
    font-weight: 700; 
    letter-spacing: 2px; 
    text-transform: uppercase; 
    color: var(--accent3); 
    margin-bottom: 12px; 
  }
  
  .analysis-body { 
    color: var(--text-secondary); 
    font-size: 0.92rem; 
    line-height: 1.8; 
  }
  
  .tag { 
    display: inline-block; 
    background: rgba(168,85,247,0.15); 
    border: 1px solid rgba(168,85,237,0.3); 
    color: var(--accent3); 
    padding: 4px 14px; 
    border-radius: 100px; 
    font-size: 0.78rem; 
    font-family: 'Space Mono', monospace; 
    margin: 3px; 
  }
  
  .warning-box { 
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    color: #fbbf24;
    font-size: 0.85rem;
    margin-top: 16px;
  }
  
  .success-box { 
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    color: #34d399;
    font-size: 0.85rem;
    margin-top: 16px;
  }
  
  .footer { 
    text-align: center;
    padding: 32px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 2px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
  }
  
  [data-testid="column"] { 
    padding: 0 8px !important; 
  }
  
  .stSpinner > div {
    border-color: var(--accent2) !important;
  }
  
  /* Responsive Design */
  @media (min-width: 1200px) {
    .hero-sub {
      max-width: 700px !important;
    }
  }
  
  @media (max-width: 768px) {
    .metric-grid {
      grid-template-columns: 1fr !important;
      gap: 12px !important;
    }
    
    .result-card {
      padding: 20px !important;
    }
    
    .hero-title {
      font-size: 1.8rem !important;
    }
    
    .hero-sub {
      font-size: 0.9rem !important;
      padding: 0 16px !important;
    }
  }
</style>
""", unsafe_allow_html=True)

# ─── Groq API ─────────────────────────────────────────────────────────────────
def analyze_startup(api_key: str, data: dict) -> dict:
    prompt = f"""
You are a world-class startup analyst with access to decades of VC research, Y Combinator data, CB Insights reports, and startup failure post-mortems. Analyze this startup idea with surgical precision based on REAL statistics and research.

STARTUP DETAILS:
- Idea / Product: {data['idea']}
- Category: {data['industry']}
- Who will use it: {data['target_market']}
- Problem Being Solved: {data['problem']}
- Why it's better: {data['uvp']}
- Revenue model: {data['business_model']}
- Team Size: {data['team_size']}
- Founder Background: {data['founder_exp']}
- Funding: {data['funding']}
- Money Available: {data['capital']}
- Launch Location: {data['geography']}
- Current Stage: {data['stage']}
- Competition: {data['competition']}
- Customer Acquisition: {data['gtm']}
- Defensibility / Moat: {data['moat']}

Provide a structured JSON analysis with the following keys:
{{
  "success_score": <integer 0-100>,
  "verdict": "<one of: HIGH_POTENTIAL | MODERATE_POTENTIAL | HIGH_RISK>",
  "one_liner": "<a punchy 1-sentence verdict under 20 words>",
  "market_analysis": "<2-3 paragraphs: market size stats, growth trends, timing>",
  "strengths": ["<strength 1 with stat/evidence>", "<strength 2>", "<strength 3>", "<strength 4>"],
  "weaknesses": ["<weakness 1 with stat/evidence>", "<weakness 2>", "<weakness 3>"],
  "key_risks": ["<risk 1>", "<risk 2>", "<risk 3>"],
  "comparable_successes": ["<company/case 1>", "<company/case 2>"],
  "comparable_failures": ["<company/case 1>", "<company/case 2>"],
  "market_score": <0-100>,
  "team_score": <0-100>,
  "timing_score": <0-100>,
  "moat_score": <0-100>,
  "actionable_advice": "<3-4 sentences of the most important things to do next, grounded in data>",
  "survival_probability_1yr": <percentage integer>,
  "survival_probability_5yr": <percentage integer>,
  "statistical_insight": "<1 powerful industry-specific stat from CB Insights, Startup Genome, or similar research>"
}}

Be brutally honest. Use real statistics. Return ONLY valid JSON, no markdown.
"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2500,
    }
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers, json=payload, timeout=90,
    )
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"): raw = raw[4:]
    return json.loads(raw.strip())


# ══════════════════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <div class="hero-badge">🔮 AI-Powered Startup Predictor</div>
  <h1 class="hero-title">Will Your Startup <span>Survive?</span></h1>
  <p class="hero-sub">Answer a few simple questions and our AI will tell you if your idea has what it takes — backed by real data and research.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-wrapper">', unsafe_allow_html=True)

# ── API Key ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">🔑</div>
  <div>
    <div class="step-title">Your Groq API Key</div>
    <div class="step-desc">Free at console.groq.com — needed to run the AI</div>
  </div>
</div>
""", unsafe_allow_html=True)
api_key = st.text_input("Paste your Groq API key here", type="password", placeholder="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxx")

# ── STEP 1 · The Idea ─────────────────────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">1</div>
  <div>
    <div class="step-title">What's Your Idea? 💡</div>
    <div class="step-desc">Describe it simply — like you're explaining to a friend</div>
  </div>
</div>
""", unsafe_allow_html=True)

idea = st.text_area(
    "Describe your startup idea",
    placeholder="Example: An app that helps students find study partners nearby who are studying the same subject...",
    height=100,
)

col1, col2 = st.columns(2)
with col1:
    industry = st.selectbox("📂 What category is it?", [
        "📱 App / Mobile",
        "🌐 Website / Online Platform",
        "🛒 Online Shop / E-Commerce",
        "💰 Money & Finance (Fintech)",
        "🏥 Health & Fitness",
        "📚 Education & Learning",
        "🎮 Games & Entertainment",
        "🤖 AI / Technology",
        "🌱 Environment & Sustainability",
        "🏠 Home & Real Estate",
        "🚗 Transport & Delivery",
        "🍕 Food & Restaurant",
        "👗 Fashion & Beauty",
        "🐾 Pets & Animals",
        "✈️ Travel & Tourism",
        "💼 Business Tools (B2B SaaS)",
        "🔬 Science & Research",
        "🎨 Art & Creativity",
        "⚽ Sports & Fitness",
        "🎓 School / University Tools",
        "📦 Logistics & Supply Chain",
        "📣 Marketing & Advertising",
        "🍃 Agriculture / Farming",
        "🔗 Crypto / Web3",
        "🚀 Space Tech",
        "🧬 Biotech / Medicine",
        "💡 Other / Not sure",
    ])

with col2:
    target_market = st.selectbox("👥 Who will use it?", [
        "👦 Kids (under 12)",
        "🧑‍🎓 Teenagers (13–17)",
        "🎒 College Students (18–22)",
        "👨 Young Adults (23–30)",
        "👩‍💼 Working Professionals (30–45)",
        "👨‍👩‍👧 Parents & Families",
        "🧓 Older Adults (50+)",
        "🏪 Small Businesses & Shops",
        "🏬 Medium-sized Companies",
        "🏙️ Large Corporations",
        "👩‍⚕️ Doctors & Healthcare Workers",
        "👩‍🏫 Teachers & Educators",
        "👨‍💻 Developers & Tech People",
        "🎨 Artists & Creators",
        "🚜 Farmers",
        "🛍️ Online Shoppers",
        "🏋️ Fitness Enthusiasts",
        "📸 Social Media Influencers",
        "💰 Investors & Traders",
        "🌍 Everyone (General Public)",
    ])

# ── STEP 2 · Problem ──────────────────────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">2</div>
  <div>
    <div class="step-title">What Problem Does It Solve? 🔥</div>
    <div class="step-desc">What pain or frustration does your idea fix?</div>
  </div>
</div>
""", unsafe_allow_html=True)

problem = st.text_area(
    "Describe the problem",
    placeholder="Example: Students waste hours searching for study partners and often end up studying alone...",
    height=85,
)
uvp = st.text_area(
    "✨ Why is YOUR solution better than what already exists?",
    placeholder="Example: Unlike Facebook groups, our app auto-matches students by subject, location, and study style...",
    height=85,
)

# ── STEP 3 · Business ─────────────────────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">3</div>
  <div>
    <div class="step-title">How Will You Make Money? 💰</div>
    <div class="step-desc">Pick the model that best fits your idea</div>
  </div>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    business_model = st.selectbox("💵 Revenue model", [
        "🆓 Free with ads",
        "💎 Free basic + paid premium (Freemium)",
        "📅 Monthly subscription fee",
        "📆 Yearly subscription fee",
        "🛒 Sell products directly",
        "🤝 Take a % cut from each transaction",
        "💳 One-time purchase",
        "📦 Pay per use",
        "🎁 Donations / crowdfunding",
        "🏛️ Government or grant funded",
        "🤲 Non-profit",
        "📋 Consulting / services",
        "🔧 Sell hardware + software together",
        "🤔 Not sure yet",
    ])

with col4:
    geography = st.selectbox("🌍 Where will you launch first?", [
        "🇮🇳 India",
        "🏙️ Just my city or town (local)",
        "🇺🇸 United States",
        "🇬🇧 United Kingdom",
        "🇪🇺 Europe",
        "🇸🇬 Southeast Asia",
        "🇦🇪 Middle East",
        "🇧🇷 Latin America",
        "🌍 Africa",
        "🌏 Australia / New Zealand",
        "🌐 Everywhere from day 1",
    ])

# ── STEP 4 · Team ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">4</div>
  <div>
    <div class="step-title">Tell Us About Your Team 👥</div>
    <div class="step-desc">Investors care a LOT about who is building this</div>
  </div>
</div>
""", unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    team_size = st.selectbox("👤 How many people are working on this?", [
        "Just me (solo founder)",
        "2 people",
        "3–5 people",
        "6–10 people",
        "11–20 people",
        "21–50 people",
        "More than 50 people",
    ])

with col6:
    founder_exp = st.selectbox("🎓 Which best describes YOU?", [
        "🧒 I'm a student (school or college)",
        "🎓 Fresh graduate — this is my first idea",
        "👶 No experience, but super passionate",
        "🛠️ I already work in this industry",
        "💼 I've worked at a big company before",
        "🚀 I've tried starting a business before (didn't succeed)",
        "✅ I've successfully built and sold a startup before",
        "🔬 I'm an expert or researcher in this field",
        "👨‍💻 I'm a developer / engineer",
        "🎨 I'm a designer or creative person",
        "📊 I have a business or finance background",
    ])

# ── STEP 5 · Money & Stage ────────────────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">5</div>
  <div>
    <div class="step-title">Money & Progress 🏦</div>
    <div class="step-desc">Where are you right now with your startup?</div>
  </div>
</div>
""", unsafe_allow_html=True)

col7, col8 = st.columns(2)
with col7:
    stage = st.selectbox("📍 What stage are you at?", [
        "💭 Just an idea in my head",
        "📝 Written a plan / business plan",
        "🛠️ Building the first version",
        "🧪 Have a working demo or MVP",
        "🙋 Have my first few users",
        "📈 Growing — making some money",
        "🚀 Scaling fast",
    ])

with col8:
    funding = st.selectbox("💳 How is it funded right now?", [
        "💸 Using my own savings / pocket money",
        "👨‍👩‍👧 Family and friends have invested",
        "🏆 Won a competition or grant",
        "🌱 Got seed funding from investors",
        "📈 Series A funding",
        "💰 Series B or beyond",
        "💹 Already making money from customers",
        "🔍 Still looking for funding",
    ])

capital_options = {
    "₹0 — just starting out": 0,
    "Less than ₹5 Lakh (under $6K)": 5000,
    "₹5L to ₹25L ($6K–$30K)": 15000,
    "₹25L to ₹1 Crore ($30K–$120K)": 75000,
    "₹1Cr to ₹5Cr ($120K–$600K)": 350000,
    "₹5Cr to ₹20Cr ($600K–$2.4M)": 1500000,
    "More than ₹20 Crore ($2.4M+)": 5000000,
}
capital_label = st.selectbox("💵 How much money do you have available?", list(capital_options.keys()))
capital = capital_options[capital_label]

# ── STEP 6 · Competition & Strategy ──────────────────────────────────────────
st.markdown("""
<div class="step-header">
  <div class="step-num">6</div>
  <div>
    <div class="step-title">Competition & Your Plan ⚔️</div>
    <div class="step-desc">Who else is doing this, and what's your strategy?</div>
  </div>
</div>
""", unsafe_allow_html=True)

competition_level = st.selectbox("⚔️ How many competitors are out there?", [
    "🟢 None — totally new idea, no one is doing this",
    "🟡 A few small or unknown competitors",
    "🟠 Some well-known competitors exist",
    "🔴 Very competitive — many players already",
    "💀 Dominated by giants like Google, Amazon, Zomato, etc.",
])
competition_names = st.text_input(
    "📝 Name your top competitors (optional — e.g. Uber, Zomato, Swiggy)",
    placeholder="Leave blank if you're not sure..."
)
competition = f"{competition_level}. Known competitors: {competition_names}" if competition_names else competition_level

moat = st.selectbox("🛡️ What makes your idea hard for others to copy?", [
    "🤔 Nothing special yet — just getting started",
    "⚡ We'll be much faster than anyone else",
    "💰 Much cheaper / more affordable price",
    "🎯 Way better quality or design",
    "🤝 Strong community or loyal fans",
    "🔒 Unique technology or patent we own",
    "📊 Special data or information no one else has",
    "🌐 Network effects (more users = even more valuable)",
    "🏷️ Strong brand people will trust and love",
    "🔄 Once people use us, it's hard to switch",
    "🤝 Exclusive deals or partnerships",
    "🌍 Deep local knowledge competitors don't have",
])

gtm = st.selectbox("🚀 How will you get your first customers?", [
    "📱 Social media (Instagram, TikTok, YouTube, etc.)",
    "👄 Word of mouth — friends tell friends",
    "🔍 Google search (SEO / show up online)",
    "📧 Email marketing",
    "🤝 Partner with other businesses",
    "🏫 Go directly to schools or colleges",
    "🏪 Door-to-door or on-ground sales",
    "🎪 Events, fairs, and exhibitions",
    "📰 News / press coverage",
    "💼 Direct sales (call/email businesses)",
    "📲 App Store (Google Play / Apple App Store)",
    "🎁 Free trial or freemium to attract users",
    "👥 Build a community (WhatsApp, Discord, etc.)",
    "🤳 Influencer marketing",
    "🏆 Startup competitions & hackathons",
])

# ── Submit ────────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
analyze_btn = st.button("🔮 Predict My Startup's Future!", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if analyze_btn:
    if not api_key:
        st.markdown('<div class="warning-box">⚠️ Please paste your Groq API key at the top first!</div>', unsafe_allow_html=True)
    elif not idea or len(idea.strip()) < 15:
        st.markdown('<div class="warning-box">⚠️ Please describe your startup idea in a bit more detail.</div>', unsafe_allow_html=True)
    elif not problem or len(problem.strip()) < 10:
        st.markdown('<div class="warning-box">⚠️ Please describe the problem you\'re solving.</div>', unsafe_allow_html=True)
    else:
        with st.spinner("🔮 Analyzing your idea with real startup data and research..."):
            try:
                result = analyze_startup(api_key, {
                    "idea": idea, "industry": industry, "target_market": target_market,
                    "problem": problem, "uvp": uvp or "Not specified",
                    "business_model": business_model, "team_size": team_size,
                    "founder_exp": founder_exp, "funding": funding,
                    "capital": f"{capital_label} (~${capital:,})",
                    "geography": geography, "stage": stage,
                    "competition": competition, "gtm": gtm, "moat": moat,
                })

                score   = result.get("success_score", 50)
                verdict = result.get("verdict", "MODERATE_POTENTIAL")
                verdict_class = {"HIGH_POTENTIAL":"verdict-success","MODERATE_POTENTIAL":"verdict-mixed","HIGH_RISK":"verdict-fail"}.get(verdict,"verdict-mixed")
                verdict_emoji = {"HIGH_POTENTIAL":"🚀","MODERATE_POTENTIAL":"⚡","HIGH_RISK":"⚠️"}.get(verdict,"⚡")
                verdict_label_map = {"HIGH_POTENTIAL":"HIGH POTENTIAL 🚀","MODERATE_POTENTIAL":"MODERATE POTENTIAL ⚡","HIGH_RISK":"HIGH RISK ⚠️"}
                verdict_text = verdict_label_map.get(verdict, verdict)
                score_color = "#10b981" if score >= 65 else ("#f59e0b" if score >= 40 else "#ef4444")

                st.markdown(f"""
                <div class="result-card">
                  <div class="{verdict_class} verdict-badge">{verdict_emoji} {verdict_text}</div>
                  <p style="color:#c4c0d8;font-size:1.05rem;font-style:italic;margin-bottom:24px;">"{result.get('one_liner','')}"</p>
                  <div class="metric-grid">
                    <div class="metric-box"><div class="metric-val" style="color:{score_color}">{score}</div><div class="metric-key">Overall Score</div></div>
                    <div class="metric-box"><div class="metric-val" style="color:#a78bfa">{result.get('survival_probability_1yr','?')}%</div><div class="metric-key">1-Year Survival</div></div>
                    <div class="metric-box"><div class="metric-val" style="color:#a78bfa">{result.get('survival_probability_5yr','?')}%</div><div class="metric-key">5-Year Survival</div></div>
                  </div>
                  <div class="divider"></div>
                  <div class="metric-grid">
                    <div class="metric-box"><div class="metric-val" style="color:#60a5fa;font-size:1.25rem">{result.get('market_score','?')}/100</div><div class="metric-key">📈 Market</div></div>
                    <div class="metric-box"><div class="metric-val" style="color:#60a5fa;font-size:1.25rem">{result.get('team_score','?')}/100</div><div class="metric-key">👥 Team</div></div>
                    <div class="metric-box"><div class="metric-val" style="color:#60a5fa;font-size:1.25rem">{result.get('timing_score','?')}/100</div><div class="metric-key">⏱️ Timing</div></div>
                  </div>
                  <div style="margin-top:14px;"><div class="metric-box"><div class="metric-val" style="color:#c084fc;font-size:1.25rem">{result.get('moat_score','?')}/100</div><div class="metric-key">🛡️ How Hard to Copy</div></div></div>
                </div>
                """, unsafe_allow_html=True)

                if result.get("statistical_insight"):
                    st.markdown(f"""
                    <div style="background:rgba(124,58,237,0.1);border-left:3px solid var(--accent2);border-radius:0 10px 10px 0;padding:16px 20px;margin-top:20px;">
                      <div style="font-family:'Space Mono',monospace;font-size:0.68rem;letter-spacing:2px;color:var(--accent3);margin-bottom:6px;">📊 RESEARCH INSIGHT</div>
                      <p style="color:#c4c0d8;font-size:0.9rem;line-height:1.7;margin:0;">{result.get('statistical_insight','')}</p>
                    </div>""", unsafe_allow_html=True)

                if result.get("market_analysis"):
                    st.markdown(f'<div class="result-card" style="margin-top:20px;"><div class="analysis-title">📈 Market Analysis</div><div class="analysis-body">{result.get("market_analysis","").replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)

                col_s, col_w = st.columns(2)
                with col_s:
                    s_items = "".join([f'<li style="margin-bottom:10px;color:#c4c0d8;font-size:0.88rem;line-height:1.6;">✅ {s}</li>' for s in result.get("strengths",[])])
                    st.markdown(f'<div class="result-card" style="margin-top:20px;"><div class="analysis-title" style="color:#34d399;">💪 What\'s Working For You</div><ul style="list-style:none;padding:0;">{s_items}</ul></div>', unsafe_allow_html=True)
                with col_w:
                    w_items = "".join([f'<li style="margin-bottom:10px;color:#c4c0d8;font-size:0.88rem;line-height:1.6;">⚠️ {w}</li>' for w in result.get("weaknesses",[])])
                    st.markdown(f'<div class="result-card" style="margin-top:20px;"><div class="analysis-title" style="color:#f87171;">🚧 What Needs Work</div><ul style="list-style:none;padding:0;">{w_items}</ul></div>', unsafe_allow_html=True)

                risks = result.get("key_risks", [])
                if risks:
                    risks_html = "".join([f'<span class="tag">⚡ {r}</span>' for r in risks])
                    st.markdown(f'<div class="result-card" style="margin-top:20px;"><div class="analysis-title" style="color:#fbbf24;">🎯 Key Risks to Watch Out For</div><div>{risks_html}</div></div>', unsafe_allow_html=True)

                col_cs, col_cf = st.columns(2)
                with col_cs:
                    c_items = "".join([f'<div style="padding:8px 0;border-bottom:1px solid var(--border);color:#c4c0d8;font-size:0.88rem;">🏆 {c}</div>' for c in result.get("comparable_successes",[])])
                    st.markdown(f'<div class="result-card" style="margin-top:20px;"><div class="analysis-title" style="color:#34d399;">✨ Similar Ideas That Succeeded</div>{c_items}</div>', unsafe_allow_html=True)
                with col_cf:
                    f_items = "".join([f'<div style="padding:8px 0;border-bottom:1px solid var(--border);color:#c4c0d8;font-size:0.88rem;">💀 {c}</div>' for c in result.get("comparable_failures",[])])
                    st.markdown(f'<div class="result-card" style="margin-top:20px;"><div class="analysis-title" style="color:#f87171;">⚰️ Similar Ideas That Failed</div>{f_items}</div>', unsafe_allow_html=True)

                if result.get("actionable_advice"):
                    st.markdown(f'<div class="result-card" style="margin-top:20px;background:linear-gradient(135deg,rgba(124,58,237,0.12),rgba(168,85,247,0.06));"><div class="analysis-title">🧭 What You Should Do Next</div><div class="analysis-body">{result.get("actionable_advice","").replace(chr(10),"<br>")}</div></div>', unsafe_allow_html=True)

                st.markdown(f'<div class="success-box">✅ Analysis done! · Powered by Groq + LLaMA-3.3-70B · {datetime.now().strftime("%B %d, %Y at %H:%M")}</div>', unsafe_allow_html=True)

            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response else "?"
                msg = {401:"❌ Wrong API key! Check it at console.groq.com", 429:"⏳ Too many requests — wait a few seconds and try again.", 500:"🛑 Server error — try again in a moment."}.get(status, f"❌ API Error ({status}): {str(e)}")
                st.markdown(f'<div class="warning-box">{msg}</div>', unsafe_allow_html=True)
            except json.JSONDecodeError:
                st.markdown('<div class="warning-box">⚠️ Couldn\'t read the AI response. Please try again!</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="warning-box">❌ Something went wrong: {str(e)}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  STARTUPORACLE · POWERED BY GROQ + LLAMA-3.3-70B · BUILT FOR DREAMERS & BUILDERS
</div>
""", unsafe_allow_html=True)