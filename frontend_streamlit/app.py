import streamlit as st
import os
import pandas as pd

# ------------------ CONFIG ------------------
st.set_page_config(page_title="VoteGuard", page_icon="🛡️", layout="wide")

# ------------------ SIDEBAR ------------------
st.sidebar.markdown("<h2 style='text-align:center;'>VoteGuard</h2>", unsafe_allow_html=True)

# Try to load local logo
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=120)
else:
    # fallback emoji logo
    st.sidebar.markdown("<h1 style='text-align:center;'>🛡️</h1>", unsafe_allow_html=True)

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "home"

# Meet the Team button in sidebar
if st.sidebar.button("👩‍💻 Meet the Team"):
    st.session_state.page = "team"

# ------------------ HOME PAGE ------------------
if st.session_state.page == "home":
    st.title("🛡️ Welcome to VoteGuard")
    st.subheader("AI-Powered Election Integrity Platform")

    st.write(
        """
        **VoteGuard** helps election monitors and citizens by:
        - Detecting polling stations with unusually high fraud risk using clustering + anomaly detection.
        - Triaging election-related news to quickly flag potential misinformation.
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Fraud Detection")
        st.write("Upload polling station CSVs and get risk scores, anomaly detection, and flagged high-risk clusters.")
        if st.button("Go to Fraud Detection"):
            st.session_state.page = "fraud"

    with col2:
        st.markdown("### 📰 News Triage")
        st.write("Paste any election-related headline or article and get AI-powered fake vs real predictions with confidence scores.")
        if st.button("Go to News Triage"):
            st.session_state.page = "news"

# ------------------ FRAUD DETECTION PAGE ------------------
elif st.session_state.page == "fraud":
    st.title("📊 Fraud Detection")
    st.write("Upload polling station data (CSV) to analyze fraud risk.")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())

        # Placeholder for ML results (mock chart)
        st.success("✅ Data uploaded! (Fraud risk analysis will be integrated here.)")

# ------------------ NEWS TRIAGE PAGE ------------------
elif st.session_state.page == "news":
    st.title("📰 News Triage")
    st.write("Paste an election-related headline or article to check authenticity.")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

    user_input = st.text_area("Enter news text here:")
    if st.button("Analyze News"):
        if user_input.strip():
            # Placeholder for backend API call
            st.success("✅ Analysis complete! (Real prediction will be integrated here.)")
            st.metric("Prediction", "Likely Real")
            st.metric("Confidence", "87%")
        else:
            st.warning("Please enter some text.")

# ------------------ TEAM PAGE ------------------
elif st.session_state.page == "team":
    st.title("👩‍💻 Meet the Team")
    st.write("The developers behind VoteGuard:")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

    team = [
        {"name": "Member 1", "role": "Frontend Developer", "img": "https://via.placeholder.com/150"},
        {"name": "Member 2", "role": "Backend Developer", "img": "https://via.placeholder.com/150"},
        {"name": "Member 3", "role": "ML Engineer", "img": "https://via.placeholder.com/150"},
        {"name": "Member 4", "role": "Data Scientist", "img": "https://via.placeholder.com/150"},
        {"name": "Member 5", "role": "UI/UX Designer", "img": "https://via.placeholder.com/150"},
    ]

    cols = st.columns(3)
    for idx, member in enumerate(team):
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div style="text-align:center; transition: transform 0.3s;"
                     onmouseover="this.style.transform='scale(1.1)';"
                     onmouseout="this.style.transform='scale(1)';">
                    <img src="{member['img']}" style="border-radius:50%; width:120px; height:120px;"><br>
                    <b>{member['name']}</b><br>
                    <span style="color:gray;">{member['role']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
