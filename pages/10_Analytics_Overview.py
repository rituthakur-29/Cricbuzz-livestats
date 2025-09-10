# pages/10_Analytics_Overview.py
import streamlit as st
import pandas as pd
import utils.path_setup  # ensures root path is available
from utils.db_connection import run_query

st.title("📈 Analytics Overview")
st.write("High-level statistics and KPIs from the cricket database.")

# --- Load Data ---
matches = run_query("SELECT * FROM matches;")
players = run_query("SELECT * FROM players;")
scores = run_query("SELECT * FROM scores;")

# --- KPIs Section ---
st.subheader("⚡ Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matches", len(matches))

with col2:
    st.metric("Total Players", len(players))

with col3:
    st.metric("Unique Teams", scores["team_name"].nunique())

with col4:
    st.metric("Total Runs (All Matches)", int(scores["runs"].sum()))

# --- Team Performance Summary ---
st.subheader("🏆 Team Performance")
team_summary = scores.groupby("team_name").agg(
    total_runs=("runs", "sum"),
    total_wickets=("wickets", "sum"),
    matches_played=("match_id", "nunique")
).reset_index()

team_summary["avg_runs_per_match"] = (
    team_summary["total_runs"] / team_summary["matches_played"]
).round(2)

st.dataframe(team_summary)

# --- Top Performers (Demo with Runs) ---
st.subheader("🔥 Top Scoring Teams")
top_teams = team_summary.sort_values(by="total_runs", ascending=False).head(5)
st.bar_chart(top_teams.set_index("team_name")["total_runs"])

# --- Roles Breakdown ---
st.subheader("👥 Player Roles Breakdown")
role_counts = players["role"].value_counts().reset_index()
role_counts.columns = ["Role", "Count"]
st.table(role_counts)

# --- Top Batsmen ---
st.subheader("🏏 Top Batsmen (by Runs)")
top_batsmen = run_query("""
SELECT p.player_name, ps.runs, m.series
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
JOIN matches m ON ps.match_id = m.match_id
ORDER BY ps.runs DESC
LIMIT 5;
""")
st.dataframe(top_batsmen)

# --- Top Bowlers ---
st.subheader("🎯 Top Bowlers (by Wickets)")
top_bowlers = run_query("""
SELECT p.player_name, ps.wickets, m.series
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
JOIN matches m ON ps.match_id = m.match_id
ORDER BY ps.wickets DESC
LIMIT 5;
""")
st.dataframe(top_bowlers)

# Runs leaderboard
st.subheader("🏏 Top Batsmen")
runs_leaderboard = run_query("""
    SELECT p.player_name, SUM(ps.runs) AS total_runs
    FROM player_stats ps
    JOIN players p ON ps.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_runs DESC
    LIMIT 10;
""")
st.dataframe(runs_leaderboard)

# Wickets leaderboard
st.subheader("🎯 Top Bowlers")
wickets_leaderboard = run_query("""
    SELECT p.player_name, SUM(ps.wickets) AS total_wickets
    FROM player_stats ps
    JOIN players p ON ps.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_wickets DESC
    LIMIT 10;
""")
st.dataframe(wickets_leaderboard)
st.write("These leaderboards highlight the top performers in batting and bowling based on cumulative statistics from the player_stats table.")