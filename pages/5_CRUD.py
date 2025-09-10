# pages/5_CRUD.py
import os
import streamlit as st
import utils.path_setup  # ensures root path is available
from utils.db_connection import run_query, execute_query

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logo_path = os.path.join(ROOT_DIR, "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=80)
else:
    st.sidebar.markdown("## 🏏 Cricbuzz LiveStats")
st.sidebar.markdown("Navigate the app below 👇")

st.title("⚙️ Players - CRUD")

# show existing
players = run_query("SELECT * FROM players;")
st.subheader("Existing players")
st.dataframe(players, use_container_width=True)

st.markdown("### ➕ Add / Upsert Player")
with st.form("add_player"):
    pid = st.text_input("Player ID")
    mid = st.text_input("Match ID")
    team = st.text_input("Team Name")
    pname = st.text_input("Player Name")
    role = st.text_input("Role")
    sub = st.form_submit_button("Add / Update Player")
    if sub:
        q = "INSERT OR REPLACE INTO players (player_id, match_id, team_name, player_name, role) VALUES (?, ?, ?, ?, ?)"
        ok = execute_query(q, (pid, mid, team, pname, role))
        if ok:
            st.success("Player added/updated.")
        else:
            st.error("Failed to add/update player.")

st.markdown("### ✏️ Update Player Role")
if not players.empty:
    sel = st.selectbox("Select player id", players["player_id"].unique().tolist())
    new_role = st.text_input("New role")
    if st.button("Update role"):
        ok = execute_query("UPDATE players SET role=? WHERE player_id=? AND match_id=?", (new_role, sel, players[players["player_id"]==sel].iloc[0]["match_id"]))
        if ok:
            st.success("Role updated.")
        else:
            st.error("Update failed.")

st.markdown("### 🗑️ Delete Player")
del_id = st.text_input("Player ID to delete")
if st.button("Delete player"):
    ok = execute_query("DELETE FROM players WHERE player_id=?", (del_id,))
    if ok:
        st.success("Player deleted.")
    else:
        st.error("Delete failed.")
