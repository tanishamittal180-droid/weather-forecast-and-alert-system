import streamlit as st
import pandas as pd
from weather_api import get_weather
from alerts import generate_alerts
from simulation import simulate_weather

st.set_page_config(page_title="Weather App", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {background-color: #f5f7fa;}
.card {
    padding:20px;
    border-radius:12px;
    background-color:white;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
    text-align:center;
}
.title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#0077b6;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="title">🌦️ Weather Forecast & Alert App</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.header("User Input")

mode = st.sidebar.selectbox("Select Mode", ["API Mode", "Simulation Mode"], key="mode_select")

city = st.sidebar.text_input("Enter City Name", "Delhi")
# ---------- FETCH DATA ----------
if st.sidebar.button("Get Weather", key="btn_fetch"):

    if mode == "API Mode":
        data = get_weather(city)

        temp = data["current_weather"]["temperature"]
        humidity = data["hourly"]["relativehumidity_2m"][0]
        rain_prob = data["hourly"]["precipitation_probability"][0]

    else:
        sim = simulate_weather()
        temp = sim["temp"]
        humidity = sim["humidity"]
        rain_prob = sim["rain_prob"]

    alerts = generate_alerts(temp, humidity, rain_prob)

    # ---------- KPI CARDS ----------
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'><h3>🌡 Temperature</h3><h2>{temp} °C</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h3>💧 Humidity</h3><h2>{humidity} %</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h3>🌧 Rain Chance</h3><h2>{rain_prob} %</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    # ---------- ALERTS ----------
    st.subheader("🚨 Weather Alerts")

    if alerts:
        for alert in alerts:
            st.error(alert)
    else:
        st.success("No Alerts - Weather is normal")

    st.markdown("---")

    # ---------- DATAFRAME ----------
    df = pd.DataFrame({
        "Temperature": [temp],
        "Humidity": [humidity],
        "Rain Probability": [rain_prob]
    })

    st.subheader("📊 Weather Data")
    st.dataframe(df)

    # ---------- CHARTS ----------
    st.subheader("📈 Weather Trends")

    chart_df = pd.DataFrame({
        "Temperature": [temp-2, temp, temp+1],
        "Humidity": [humidity-5, humidity, humidity+3]
    })

    st.line_chart(chart_df)

    # ---------- DOWNLOAD ----------
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Report",
        data=csv,
        file_name="weather_report.csv",
        mime="text/csv"
    )