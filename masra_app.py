# masra_app.py
import streamlit as st
from textblob import TextBlob

# ---------- SETTINGS ----------
st.set_page_config(page_title="MaSRA Pro", layout="wide")

# ---------- MOCK NEWS FETCHER ----------
mock_headlines = [
    "Federal Reserve signals further interest rate hikes",
    "US inflation eases to 2.3% in latest CPI report",
    "Tensions escalate in Taiwan Strait after military drills",
    "OPEC announces oil production cuts amid falling prices",
    "US job growth slows sharply, unemployment ticks up"
]

# ---------- MACRO TOPIC CLASSIFIER ----------
macro_keywords = {
    'interest rates': ['rate hike', 'federal reserve', 'interest rate'],
    'inflation': ['inflation', 'cpi', 'consumer price'],
    'geopolitical tension': ['tensions', 'war', 'conflict', 'china', 'drills'],
    'oil prices': ['oil', 'opec', 'production cuts'],
    'job market': ['job market', 'unemployment', 'jobs report']
}

def classify_macro_topic(text):
    for topic, keywords in macro_keywords.items():
        if any(keyword in text.lower() for keyword in keywords):
            return topic
    return "unknown"

# ---------- SENTIMENT ANALYZER ----------
def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

# ---------- RISK SIMULATOR ----------
macro_impact_matrix = {
    'interest rates': {'Tech': -1, 'Financials': 1, 'Energy': 0, 'Bonds': -1, 'Gold': 1},
    'inflation': {'Tech': -1, 'Financials': 0, 'Energy': 1, 'Bonds': -1, 'Gold': 1},
    'geopolitical tension': {'Tech': -1, 'Financials': -1, 'Energy': 1, 'Bonds': 1, 'Gold': 1},
    'oil prices': {'Tech': 0, 'Financials': 0, 'Energy': 1, 'Bonds': -1, 'Gold': 1},
    'job market': {'Tech': 1, 'Financials': 1, 'Energy': 0, 'Bonds': -1, 'Gold': 0}
}

default_portfolio = [
    {'ticker': 'AAPL', 'sector': 'Tech', 'weight': 0.25},
    {'ticker': 'JPM', 'sector': 'Financials', 'weight': 0.20},
    {'ticker': 'XLE', 'sector': 'Energy', 'weight': 0.15},
    {'ticker': 'TLT', 'sector': 'Bonds', 'weight': 0.25},
    {'ticker': 'GLD', 'sector': 'Gold', 'weight': 0.15}
]

def simulate_risk(portfolio, macro_topic):
    if macro_topic not in macro_impact_matrix:
        return 0, ["Unknown macro topic."]
    
    impact = 0
    breakdown = []
    for asset in portfolio:
        sector = asset['sector']
        weight = asset['weight']
        effect = macro_impact_matrix[macro_topic].get(sector, 0)
        score = weight * effect
        impact += score
        breakdown.append(f"{asset['ticker']} ({sector}): {'+' if score >= 0 else ''}{score:.2f}")
    return impact, breakdown

# ---------- RECOMMENDER ----------
def get_recommendation(risk_score, topic):
    if abs(risk_score) < 0.1:
        return "🟢 Risk neutral. No urgent action required."
    elif risk_score > 0:
        return f"🔴 Risk increasing due to {topic}. Consider hedging with Gold or Bonds."
    else:
        return f"🟢 Risk decreasing due to {topic}. Potential opportunity to expand in Tech or Financials."

# ---------- STREAMLIT UI ----------
st.title("📊 MaSRA Pro — Macro Sentiment Risk Adjuster")
st.markdown("A professional real-time macro-risk analysis tool for portfolios 💼")

# Sidebar
st.sidebar.header("📰 Sample Headlines")
selected_headline = st.sidebar.selectbox("Pick a headline to analyze:", mock_headlines)

# Analysis button
if st.sidebar.button("🔍 Run Analysis"):
    topic = classify_macro_topic(selected_headline)
    sentiment = analyze_sentiment(selected_headline)
    risk_score, breakdown = simulate_risk(default_portfolio, topic)
    recommendation = get_recommendation(risk_score, topic)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🧠 Detected Topic")
        st.info(topic)
        st.subheader("😊 Sentiment Score")
        st.write(f"{sentiment:.2f}")

    with col2:
        st.subheader("📉 Risk Score")
        st.write(f"{risk_score:.2f}")
        st.subheader("📢 AI Recommendation")
        st.success(recommendation)

    st.markdown("---")
    st.subheader("📦 Portfolio Impact Breakdown")
    for line in breakdown:
        st.markdown(f"- {line}")

else:
    st.info("Use the sidebar to select a headline and run analysis.")
