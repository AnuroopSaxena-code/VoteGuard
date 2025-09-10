import streamlit as st
import pandas as pd
import plotly.express as px
from api_client import health_check, predict_fraud, predict_news

# ----- PAGE CONFIG -----
st.set_page_config(page_title="VoteGuard", layout="wide")

# ----- SIDEBAR -----
st.sidebar.title("🛡️ VoteGuard")
if st.sidebar.button("Check Backend Health"):
    try:
        resp = health_check()
        st.sidebar.success(f"Backend says: {resp}")
    except Exception as e:
        st.sidebar.error(f"Health check failed: {e}")

st.sidebar.markdown("---")
st.sidebar.write("Built at [Hackathon Name] 🏆")
st.sidebar.write("Team: <your team name>")

# ----- MAIN APP -----
tab1, tab2 = st.tabs(["Fraud Detection", "News Triage"])

# ====================
# TAB 1 - FRAUD
# ====================
with tab1:
    st.header("📊 Polling Station Risk Analysis")

    uploaded_file = st.file_uploader("Upload polling station CSV", type=["csv"])
    if uploaded_file is not None:
        with st.spinner("Analyzing..."):
            try:
                results = predict_fraud(uploaded_file)
            except Exception as e:
                st.error(f"API error: {e}")
                results = None

        if results:
            stations = pd.DataFrame(results["stations"])
            clusters = results.get("clusters", [])

            # KPIs
            total = len(stations)
            critical = (stations["risk_bucket"] == "Critical").sum()
            high_plus = (stations["risk_bucket"].isin(["High", "Critical"])).mean() * 100

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Stations", total)
            col2.metric("% High+Critical", f"{high_plus:.1f}%")
            col3.metric("# Critical", critical)

            # Leaderboard
            st.subheader("Leaderboard")
            st.dataframe(
                stations[["station_id", "district", "state", "risk_score", "risk_bucket"]],
                use_container_width=True
            )

            # Scatterplot
            st.subheader("Cluster Scatter")
            fig = px.scatter(
                stations,
                x="z_turnout",
                y="z_invalid",
                size="risk_score",
                color="cluster_id",
                hover_data=["station_id", "risk_bucket", "risk_score"],
                title="Stations by Turnout vs Invalid Votes"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Drilldown
            selected_id = st.selectbox("Select station for details", stations["station_id"])
            st.write("Station Details:")
            st.json(stations[stations["station_id"] == selected_id].to_dict(orient="records")[0])

# ====================
# TAB 2 - NEWS
# ====================
with tab2:
    st.header("📰 News Headline Triage")
    headline = st.text_area("Paste a headline to analyze")
    if st.button("Analyze Headline"):
        with st.spinner("Checking..."):
            try:
                result = predict_news(headline)
                st.success(f"Label: {result['label']}, Confidence: {result['confidence']:.2f}")
            except Exception as e:
                st.error(f"API error: {e}")
