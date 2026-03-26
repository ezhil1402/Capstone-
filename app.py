import streamlit as st
import pandas as pd
import plotly.express as px
from models import StudySession, ScheduleManager, BurnoutAnalyzer, RecommendationEngine
from utils import save_data, load_data

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Smart Study Planner", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 Smart Planner")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Add Session", "Analytics"])

# ---------- LOAD DATA ----------
df = load_data()

# ---------- DASHBOARD ----------
if menu == "Dashboard":
    st.title("📊 Dashboard")

    total_hours = df["Hours"].sum() if not df.empty else 0
    total_break = df["Break"].sum() if not df.empty else 0
    sessions = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Study Hours", total_hours)
    col2.metric("Total Break Time", total_break)
    col3.metric("Total Sessions", sessions)

    st.divider()

    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Study Hours by Subject")
            fig = px.bar(df, x="Subject", y="Hours", color="Subject")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Break vs Study")
            fig2 = px.scatter(df, x="Hours", y="Break", size="Hours", color="Subject")
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Recent Activity")
    st.dataframe(df.tail(5), use_container_width=True)

# ---------- ADD SESSION ----------
elif menu == "Add Session":
    st.title("➕ Add Study Session")

    with st.form("study_form"):
        name = st.text_input("Name")
        subject = st.text_input("Subject")

        col1, col2 = st.columns(2)
        hours = col1.number_input("Study Hours", 0.0, 12.0)
        break_time = col2.number_input("Break Time", 0.0, 5.0)

        submit = st.form_submit_button("Save Session")

    if submit:
        if name and subject:
            session = StudySession(subject, hours, break_time)
            manager = ScheduleManager()
            manager.add_session(session)

            save_data(name, subject, hours, break_time)

            analyzer = BurnoutAnalyzer()
            risk = analyzer.analyze(manager.total_study_hours(), manager.total_break_time())

            recommender = RecommendationEngine()
            suggestion = recommender.suggest(risk)

            st.success("✅ Session Saved!")
            st.subheader(f"Burnout Risk: {risk}")
            st.info(suggestion)

        else:
            st.error("Please fill all fields")

# ---------- ANALYTICS ----------
elif menu == "Analytics":
    st.title("📊 Analytics")

    if df.empty:
        st.warning("No data available")
    else:
        tab1, tab2 = st.tabs(["📚 Subject Analysis", "⏳ Trend"])

        with tab1:
            fig = px.pie(df, names="Subject", values="Hours", title="Study Distribution")
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            df["Session"] = range(1, len(df) + 1)
            fig2 = px.line(df, x="Session", y="Hours", title="Study Trend")
            st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        st.subheader("Full Dataset")
        st.dataframe(df, use_container_width=True)