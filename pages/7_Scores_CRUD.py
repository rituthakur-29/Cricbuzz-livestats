# pages/7_Scores_CRUD.py
import os
import streamlit as st
from utils.db_connection import run_query, execute_query

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logo_path = os.path.join(ROOT_DIR, "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=80)
else:
    st.sidebar.markdown("## 🏏 Cricbuzz LiveStats")
st.sidebar.markdown("Navigate the app below 👇")

st.title("⚙️ Scores - CRUD")

scores = run_query("SELECT * FROM scores;")
st.subheader("Existing Scores")
st.dataframe(scores, use_container_width=True)

st.markdown("### ➕ Add Score")
with st.form("add_score"):
    mid = st.text_input("Match ID")
    team = st.text_input("Team Name")
    runs = st.number_input("Runs", min_value=0)
    wickets = st.number_input("Wickets", min_value=0)
    overs = st.number_input("Overs", min_value=0.0, step=0.1)
    if st.form_submit_button("Add Score"):
        ok = execute_query(
            "INSERT INTO scores (match_id, team_name, runs, wickets, overs) VALUES (?, ?, ?, ?, ?)",
            (mid, team, runs, wickets, overs)
        )
        st.success("Score added." if ok else "Failed.")
