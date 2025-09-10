# pages/9_Visualizations.py
import streamlit as st
import pandas as pd
import plotly.express as px
import utils.path_setup  # ensures root path is available
from utils.db_connection import run_query


st.title("📊 Cricket Visualizations")
st.write("Explore interactive insights from the cricket database.")

# --- Load Data ---
matches = run_query("SELECT * FROM matches;")
players = run_query("SELECT * FROM players;")
scores = run_query("SELECT * FROM scores;")

# --- Filter Sidebar ---
st.sidebar.subheader("🔍 Filters")
selected_series = st.sidebar.multiselect(
    "Select Series", matches["series"].unique(), default=matches["series"].unique()
)
selected_teams = st.sidebar.multiselect(
    "Select Teams", scores["team_name"].unique(), default=scores["team_name"].unique()
)

# Filtered Data
matches_filtered = matches[matches["series"].isin(selected_series)]
scores_filtered = scores[scores["team_name"].isin(selected_teams)]

# --- Chart 1: Runs Comparison (Bar Chart) ---
st.subheader("🏏 Runs by Team")
if not scores_filtered.empty:
    fig1 = px.bar(
        scores_filtered,
        x="team_name",
        y="runs",
        color="team_name",
        barmode="group",
        title="Total Runs Scored by Teams",
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No runs data available for selected filters.")

# --- Chart 2: Wickets Taken (Bar Chart) ---
st.subheader("🎯 Wickets by Team")
if "wickets" in scores_filtered.columns:
    fig2 = px.bar(
        scores_filtered,
        x="team_name",
        y="wickets",
        color="team_name",
        title="Total Wickets by Teams",
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Chart 3: Player Roles Distribution (Pie Chart) ---
st.subheader("👥 Player Roles Distribution")
if not players.empty:
    role_counts = players["role"].value_counts().reset_index()
    role_counts.columns = ["role", "count"]
    fig3 = px.pie(role_counts, values="count", names="role", title="Player Roles Breakdown")
    st.plotly_chart(fig3, use_container_width=True)

# --- Chart 4: Matches Timeline (Line Chart) ---
st.subheader("📅 Matches Over Time")
if not matches_filtered.empty:
    matches_filtered["date"] = pd.to_datetime(matches_filtered["date"])
    fig4 = px.line(
        matches_filtered,
        x="date",
        y="match_id",
        markers=True,
        title="Matches Played Over Time",
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------

st.subheader("📊 Additional Visuals (Player Stats)")

# Runs leaderboard
batsmen_chart = run_query("""
    SELECT p.player_name, SUM(ps.runs) AS total_runs
    FROM player_stats ps
    JOIN players p ON ps.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_runs DESC
    LIMIT 5;
""")
if not batsmen_chart.empty:
    st.bar_chart(batsmen_chart.set_index("player_name"))

# Wickets leaderboard
bowlers_chart = run_query("""
    SELECT p.player_name, SUM(ps.wickets) AS total_wickets
    FROM player_stats ps
    JOIN players p ON ps.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_wickets DESC
    LIMIT 5;
""")
if not bowlers_chart.empty:
    st.bar_chart(bowlers_chart.set_index("player_name"))
    st.write("Data visualizations are based on the current database entries.")