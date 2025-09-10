# pages/2_Players.py
import os
import streamlit as st
import utils.path_setup  # ensures root path is available
from utils.db_connection import run_query


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logo_path = os.path.join(ROOT_DIR, "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=80)
else:
    st.sidebar.markdown("## 🏏 Cricbuzz LiveStats")
st.sidebar.markdown("Navigate the app below 👇")

st.title("👥 Players Overview")

players = run_query("SELECT * FROM players;")
if players.empty:
    st.warning("No players in DB.")
else:
    match_ids = players["match_id"].unique().tolist()
    selected_match = st.selectbox("Filter by Match ID (optional)", ["All"] + match_ids)
    if selected_match == "All":
        st.dataframe(players, use_container_width=True)
    else:
        st.dataframe(players[players["match_id"] == selected_match], use_container_width=True)

# --- Top Performers from player_stats ---
import streamlit as st
from utils.db_connection import run_query

st.subheader("🏆 Top Performers (from Player Stats)")

# Top batsmen (by total runs)
top_batsmen = run_query("""
    SELECT p.player_name, SUM(ps.runs) AS total_runs
    FROM player_stats ps
    JOIN players p ON ps.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_runs DESC
    LIMIT 5;
""")
st.write("### 🔝 Top 5 Batsmen (Runs)")
st.dataframe(top_batsmen)

# Top bowlers (by total wickets)
top_bowlers = run_query("""
    SELECT p.player_name, SUM(ps.wickets) AS total_wickets
    FROM player_stats ps
    JOIN players p ON ps.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_wickets DESC
    LIMIT 5;
""")
st.write("### 🎯 Top 5 Bowlers (Wickets)")
st.dataframe(top_bowlers)
