import streamlit as st
import pandas as pd
from models import StudySession, ScheduleManager, BurnoutAnalyzer, RecommendationEngine
from utils import save_data, load_data

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="Study Planner", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("📚 Smart Study Planner")
menu = st.sidebar.radio("Go to", ["Dashboard", "Add Session", "Analytics"])

# ---------- LOAD DATA ----------
df = load_data()

# ---------- DASHBOARD ----------
if menu == "Dashboard":
    st.title("📊 Dashboard")

    if df.empty:
        st.warning("No data available")
    else:
        total_hours = df["Hours"].sum()
        total_break = df["Break"].sum()
        total_sessions = len(df)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Study Hours", total_hours)
        col2.metric("Total Break Time", total_break)
        col3.metric("Total Sessions", total_sessions)

        st.divider()

        st.subheader("Study Hours by Subject")
        chart_data = df.groupby("Subject")["Hours"].sum()
        st.bar_chart(chart_data)

# ---------- ADD SESSION ----------
elif menu == "Add Session":
    st.title("➕ Add Study Session")

    name = st.text_input("Enter Name")
    subject = st.text_input("Enter Subject")
    hours = st.number_input("Study Hours", min_value=0.0, max_value=12.0)
    break_time = st.number_input("Break Time", min_value=0.0, max_value=5.0)

    if st.button("Save Session"):
        if name and subject:
            session = StudySession(subject, hours, break_time)

            manager = ScheduleManager()
            manager.add_session(session)

            save_data(name, subject, hours, break_time)

            analyzer = BurnoutAnalyzer()
            risk = analyzer.analyze(manager.total_study_hours(), manager.total_break_time())

            recommender = RecommendationEngine()
            suggestion = recommender.suggest(risk)

            st.success("✅ Session saved successfully!")
            st.write("### Burnout Risk:", risk)
            st.info(suggestion)

        else:
            st.error("Please fill all fields")

# ---------- ANALYTICS ----------
elif menu == "Analytics":
    st.title("📊 Analytics")

    if df.empty:
        st.warning("No data available")
    else:
        st.subheader("Study Distribution")
        st.bar_chart(df.groupby("Subject")["Hours"].sum())

        st.subheader("Break Time Analysis")
        st.line_chart(df.groupby("Subject")["Break"].sum())

        st.subheader("All Data")
        st.dataframe(df)