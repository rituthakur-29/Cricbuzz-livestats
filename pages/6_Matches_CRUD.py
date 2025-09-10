# pages/6_Matches_CRUD.py
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

st.title("⚙️ Matches - CRUD")

matches = run_query("SELECT * FROM matches;")
st.subheader("Existing Matches")
st.dataframe(matches, use_container_width=True)

st.markdown("### ➕ Add Match")
with st.form("add_match"):
    mid = st.text_input("Match ID")
    series = st.text_input("Series")
    fmt = st.text_input("Format")
    venue = st.text_input("Venue")
    date = st.date_input("Date")
    status = st.text_input("Status")
    if st.form_submit_button("Add Match"):
        ok = execute_query(
            "INSERT OR REPLACE INTO matches (match_id, series, format, venue, date, status) VALUES (?, ?, ?, ?, ?, ?)",
            (mid, series, fmt, venue, str(date), status)
        )
        st.success("Match added." if ok else "Failed.")
