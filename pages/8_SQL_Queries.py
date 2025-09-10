import streamlit as st
from utils.db_connection import run_query
import pandas as pd

st.sidebar.title("🏏 Cricbuzz LiveStats")
st.sidebar.markdown("Navigate through the app using the menu below 👇")

st.title("🔍 SQL Query Interface")

# --- Helper to render tables + charts ---
def render_result(result: pd.DataFrame):
    if result.empty:
        st.warning("⚠️ No results found.")
    else:
        st.dataframe(result, use_container_width=True)
        # Auto-draw chart if numeric columns exist
        numeric_cols = result.select_dtypes(include=["int64", "float64"]).columns
        if len(numeric_cols) > 0:
            st.bar_chart(result.set_index(result.columns[0])[numeric_cols])

# --- Tabs for levels ---
tab1, tab2, tab3 = st.tabs(["🌱 Beginner (Q1–Q8)", "⚡ Intermediate (Q9–Q16)", "🚀 Advanced (Q17–Q25)"])

# ---------------- Beginner Queries ----------------
with tab1:
    st.subheader("Beginner Queries (Q1–Q8)")
    beginner_queries = {
        "1. Find all players who represent India":
            "SELECT player_name, role FROM players WHERE team_name='India';",

        "2. Show all cricket matches (last 30 days demo)":
            "SELECT match_id, series, date, venue, status FROM matches ORDER BY date DESC;",

        "3. Top 10 run scorers (team-wise demo)":
            "SELECT team_name, SUM(runs) as total_runs FROM scores GROUP BY team_name ORDER BY total_runs DESC LIMIT 10;",

        "4. Venues with matches (capacity not in mock data)":
            "SELECT DISTINCT venue FROM matches;",

        "5. How many matches each team has won (demo)":
            "SELECT team_name, COUNT(*) as wins FROM scores GROUP BY team_name ORDER BY wins DESC;",

        "6. Count of players by role":
            "SELECT role, COUNT(*) as player_count FROM players GROUP BY role;",

        "7. Highest runs scored in each match (mock for format-based)":
            "SELECT match_id, MAX(runs) as highest_score FROM scores GROUP BY match_id;",

        "8. Show all cricket series in 2025":
            "SELECT match_id, series, venue, date FROM matches WHERE date LIKE '2025%';"
    }

    choice = st.selectbox("Pick a Beginner Query", list(beginner_queries.keys()), key="beginner")
    if st.button("Run Beginner Query"):
        result = run_query(beginner_queries[choice])
        render_result(result)

# ---------------- Intermediate Queries ----------------
with tab2:
    st.subheader("Intermediate Queries (Q9–Q16)")
    intermediate_queries = {
        "9. All-rounders with 1000+ runs AND 50+ wickets (demo)":
            "SELECT player_name, team_name, role FROM players WHERE role='All-rounder';",

        "10. Last 20 completed matches (demo)":
            "SELECT match_id, series, date, venue, status FROM matches ORDER BY date DESC LIMIT 20;",

        "11. Compare player runs across formats (demo)":
            "SELECT player_name, team_name, role FROM players ORDER BY player_name;",

        "12. Team performance Home vs Away (mock)":
            "SELECT team_name, COUNT(*) as matches_played FROM scores GROUP BY team_name;",

        "13. Batting partnerships 100+ (demo)":
            "SELECT match_id, SUM(runs) as total_runs FROM scores GROUP BY match_id HAVING total_runs > 100;",

        "14. Bowling performance at venues (demo)":
            "SELECT team_name, SUM(wickets) as total_wickets FROM scores GROUP BY team_name;",

        "15. Players in close matches (demo filter)":
            "SELECT match_id, team_name, runs FROM scores WHERE runs BETWEEN 150 AND 200;",

        "16. Player performance per year (demo)":
            "SELECT player_name, team_name FROM players ORDER BY player_name;"
    }

    choice = st.selectbox("Pick an Intermediate Query", list(intermediate_queries.keys()), key="intermediate")
    if st.button("Run Intermediate Query"):
        result = run_query(intermediate_queries[choice])
        render_result(result)

# ---------------- Advanced Queries ----------------
with tab3:
    st.subheader("Advanced Queries (Q17–Q25)")
    advanced_queries = {
        "17. Toss advantage analysis (mock)":
            "SELECT match_id, status FROM matches;",

        "18. Most economical bowlers (demo)":
            "SELECT team_name, SUM(wickets) as wickets FROM scores GROUP BY team_name;",

        "19. Consistent batsmen (demo)":
            "SELECT player_name, team_name FROM players ORDER BY player_name;",

        "20. Matches count per player (demo)":
            "SELECT player_name, role FROM players;",

        "21. Player performance ranking (mock)":
            "SELECT player_name, team_name FROM players;",

        "22. Head-to-head team analysis (demo)":
            "SELECT match_id, series, status FROM matches;",

        "23. Recent player form (demo)":
            "SELECT player_name, role FROM players WHERE role='Batsman';",

        "24. Successful batting partnerships (demo)":
            "SELECT match_id, SUM(runs) as total_runs FROM scores GROUP BY match_id;",

        "25. Player time-series performance (mock)":
            "SELECT player_name, team_name FROM players;"
    }

    choice = st.selectbox("Pick an Advanced Query", list(advanced_queries.keys()), key="advanced")
    if st.button("Run Advanced Query"):
        result = run_query(advanced_queries[choice])
        render_result(result)

# ---------------- Free-form Query ----------------
st.subheader("📝 Or run your own query")
query = st.text_area("Enter SQL query:", "SELECT * FROM matches;")
if st.button("Run Custom Query"):
    result = run_query(query)
    render_result(result)
