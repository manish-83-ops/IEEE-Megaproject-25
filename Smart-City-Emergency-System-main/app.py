# ===============================
# SMART CITY EMERGENCY INTELLIGENCE DASHBOARD
# Hackathon-Ready | High-Impact UI | Streamlit
# ===============================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import folium
from streamlit_folium import st_folium
import time

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart City Emergency Command Center",
    page_icon="🚨",
    layout="wide"
)

# ===============================
# LOAD MODEL
# ===============================
model = joblib.load("rf_model.pkl")
FEATURE_COLUMNS = joblib.load("feature_columns.pkl")

# ===============================
# CUSTOM CSS (ANIMATIONS + UI)
# ===============================
st.markdown("""
<style>
body { background-color: #0e1117; }
.big-title { font-size:40px; font-weight:800; color:#ff4b4b; }
.sub { color:#cfcfcf; }
.card {
    background: linear-gradient(135deg, #1f2933, #111827);
    padding:20px;
    border-radius:15px;
    box-shadow:0 0 20px rgba(255,75,75,0.3);
    transition: transform 0.3s ease;
}
.card:hover { transform: scale(1.03); }
.blink {
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0.3; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR NAVIGATION
# ===============================
st.sidebar.markdown("## ☰ Navigation")
page = st.sidebar.radio("", ["🚨 Command Dashboard", "🗺️ Zone Intelligence", "🚑 Resources", "📖 Story"])

# ===============================
# SIDEBAR INPUTS
# ===============================
st.sidebar.markdown("---")
st.sidebar.markdown("### ⏱️ Scenario Controls")
zone_id = st.sidebar.slider("Zone ID", 1, 14, 5)
hour = st.sidebar.slider("Hour of Day", 0, 23, 12)
day = st.sidebar.selectbox("Day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])

is_weekend = 1 if day in ["Saturday","Sunday"] else 0
day_map = {"Monday":0,"Tuesday":1,"Wednesday":2,"Thursday":3,"Friday":4,"Saturday":5,"Sunday":6}

# ===============================
# MODEL INPUT
# ===============================
input_df = pd.DataFrame([[zone_id, hour, day_map[day], is_weekend]], columns=FEATURE_COLUMNS)
prediction = model.predict(input_df)[0]

# ===============================
# INTELLIGENCE ENGINE
# ===============================
def intelligence(pred):
    if pred >= 7:
        return "🚨 MASS INCIDENT RISK — Deploy full emergency stack immediately", 3, 2, 1, "HIGH"
    elif pred >= 4:
        return "⚠️ Elevated risk — Keep rapid response teams on standby", 2, 1, 0, "MEDIUM"
    else:
        return "✅ Normal conditions — Routine monitoring sufficient", 1, 0, 0, "LOW"

intel_text, amb, pol, fire, level = intelligence(prediction)

# ===============================
# COMMAND DASHBOARD
# ===============================
if page == "🚨 Command Dashboard":
    st.markdown("<div class='big-title'>🚨 Smart City Emergency Command Center</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Real-time AI-driven incident forecasting & response planning</div>", unsafe_allow_html=True)
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='card'>📍 Zone<br><h2>{zone_id}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'>📊 Predicted Incidents<br><h2>{prediction:.2f}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'>🚦 Alert Level<br><h2 class='blink'>{level}</h2></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='card'>🧠 AI Status<br><h3>ACTIVE</h3></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### 🧠 Intelligence Briefing")
    st.success(intel_text)

    st.markdown("### 🚑 Auto Deployment Plan")
    d1, d2, d3 = st.columns(3)
    d1.markdown(f"<div class='card'>🚑 Ambulances<br><h2>{amb}</h2></div>", unsafe_allow_html=True)
    d2.markdown(f"<div class='card'>🚓 Police Units<br><h2>{pol}</h2></div>", unsafe_allow_html=True)
    d3.markdown(f"<div class='card'>🔥 Fire Units<br><h2>{fire}</h2></div>", unsafe_allow_html=True)

# ===============================
# ZONE MAP INTELLIGENCE
# ===============================
if page == "🗺️ Zone Intelligence":
    st.markdown("<div class='big-title'>🗺️ Ranchi Zone Risk Map</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub'>Heat-based incident intensity by zone</div>", unsafe_allow_html=True)

    base_map = folium.Map(location=[23.3441, 85.3096], zoom_start=12)

    np.random.seed(hour + zone_id)
    for z in range(1, 15):
        risk = model.predict(pd.DataFrame([[z, hour, day_map[day], is_weekend]], columns=FEATURE_COLUMNS))[0]
        color = "green" if risk < 4 else "orange" if risk < 7 else "red"
        folium.CircleMarker(
            location=[23.3441 + np.random.uniform(-0.05,0.05), 85.3096 + np.random.uniform(-0.05,0.05)],
            radius=10,
            color=color,
            fill=True,
            popup=f"Zone {z} | Incidents: {risk:.2f}"
        ).add_to(base_map)

    st_folium(base_map, width=900, height=500)

# ===============================
# RESOURCES PAGE
# ===============================
if page == "🚑 Resources":
    st.markdown("<div class='big-title'>🚑 Emergency Resources</div>", unsafe_allow_html=True)
    st.markdown("---")
    r1, r2, r3 = st.columns(3)
    r1.image("assets/ambulance.png", width=250)
    r1.success("Ambulance Fleet Active")

    r2.image("assets/police.jpg", width=250)
    r2.info("Police Units Patrolling")

    r3.image("assets/fire.jpg", width=250)
    r3.warning("Fire & Rescue Ready")

# ===============================
# STORY PAGE
# ===============================
if page == "📖 Story":
    st.markdown("<div class='big-title'>📖 Hackathon Story</div>", unsafe_allow_html=True)
    st.markdown("""
    ### 🚨 Problem
    Cities react **after** disasters — not before.

    ### 🧠 Solution
    AI predicts **where & when incidents occur** and auto-plans emergency response.

    ### 🌍 Impact
    - Faster response times
    - Reduced casualties
    - Smart city readiness

    ### 🏆 Why We Win
    ✔ Real ML
    ✔ Visual Intelligence
    ✔ Decision Automation
    ✔ Scalable to any city
    """)

st.markdown("---")
st.caption("Built for Hackathon | Smart City Emergency AI System")
