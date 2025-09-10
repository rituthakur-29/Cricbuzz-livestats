# streamlit_app.py
import streamlit as st
import os

st.set_page_config(page_title="🏏 Cricbuzz LiveStats", layout="wide")

ROOT_DIR = os.getcwd()
logo_path = os.path.join(ROOT_DIR, "logo.png")

if os.path.exists(logo_path):
    st.image(logo_path, width=120)
else:
    st.title("🏏 Cricbuzz LiveStats")

st.title("Welcome — Cricbuzz LiveStats")
st.write("""
This demo app is a multi-page Streamlit project showing:
- Matches, Players, Scores tables (from SQLite)
- A SQL query interface
- CRUD pages (add/update/delete)
- Visualizations with filters and CSV export

Use the sidebar to navigate to each module.
""")
st.write("Developed by Ritu Thakur")