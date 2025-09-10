# pages/3_Scores.py
import os
import streamlit as st
import plotly.express as px
import utils.path_setup  # ensures root path is available
from utils.db_connection import run_query

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logo_path = os.path.join(ROOT_DIR, "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=80)
else:
    st.sidebar.markdown("## 🏏 Cricbuzz LiveStats")
st.sidebar.markdown("Navigate the app below 👇")

st.title("📊 Scores & Quick Visuals")

scores = run_query("SELECT * FROM scores;")
if scores.empty:
    st.warning("No score entries yet.")
else:
    st.dataframe(scores, use_container_width=True)
    match_ids = scores["match_id"].unique().tolist()
    selected = st.selectbox("Select Match ID", match_ids)
    ms = scores[scores["match_id"] == selected]
    st.subheader("Scorecard")
    st.dataframe(ms, use_container_width=True)

    # simple Plotly bar
    fig = px.bar(ms, x="team_name", y="runs", text="wickets", title=f"Runs for {selected}")
    st.plotly_chart(fig, use_container_width=True)
