# utils/create_db.py
import sqlite3
import json

DB_PATH = "cricket.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop old tables (for a fresh start each run)
    cursor.executescript("""
    DROP TABLE IF EXISTS matches;
    DROP TABLE IF EXISTS players;
    DROP TABLE IF EXISTS scores;
    DROP TABLE IF EXISTS player_stats;
    """)

    # Matches table
    cursor.execute("""
    CREATE TABLE matches (
        match_id TEXT PRIMARY KEY,
        series TEXT,
        format TEXT,
        venue TEXT,
        date TEXT,
        status TEXT
    )
    """)

    # Players table
    cursor.execute("""
    CREATE TABLE players (
        player_id TEXT PRIMARY KEY,
        match_id TEXT,
        team_name TEXT,
        player_name TEXT,
        role TEXT,
        FOREIGN KEY(match_id) REFERENCES matches(match_id)
    )
    """)

    # Scores table
    cursor.execute("""
    CREATE TABLE scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT,
        team_name TEXT,
        runs INTEGER,
        wickets INTEGER,
        overs REAL,
        FOREIGN KEY(match_id) REFERENCES matches(match_id)
    )
    """)

    # Player Stats table (NEW)
    cursor.execute("""
    CREATE TABLE player_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id TEXT,
        player_id TEXT,
        runs INTEGER,
        wickets INTEGER,
        FOREIGN KEY(match_id) REFERENCES matches(match_id),
        FOREIGN KEY(player_id) REFERENCES players(player_id)
    )
    """)

    conn.commit()
    conn.close()


def insert_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open("sample_cricket_data.json", "r") as f:
        data = json.load(f)

    for match in data["matches"]:
        # Insert match
        cursor.execute("""
        INSERT INTO matches (match_id, series, format, venue, date, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (match["match_id"], match["series"], match["format"], match["venue"], match["date"], match["status"]))

        # Insert players
        for team in ["team1", "team2"]:
            team_name = match["teams"][team]["name"]
            for p in match["teams"][team]["players"]:
                cursor.execute("""
                INSERT INTO players (player_id, match_id, team_name, player_name, role)
                VALUES (?, ?, ?, ?, ?)
                """, (p["id"], match["match_id"], team_name, p["name"], p["role"]))

        # Insert team scores
        for team in ["team1", "team2"]:
            team_name = match["teams"][team]["name"]
            score = match["score"][team]
            cursor.execute("""
            INSERT INTO scores (match_id, team_name, runs, wickets, overs)
            VALUES (?, ?, ?, ?, ?)
            """, (match["match_id"], team_name, score["runs"], score["wickets"], score["overs"]))

        # Insert player stats
        if "player_stats" in match:
            for ps in match["player_stats"]:
                cursor.execute("""
                INSERT INTO player_stats (match_id, player_id, runs, wickets)
                VALUES (?, ?, ?, ?)
                """, (ps["match_id"], ps["player_id"], ps["runs"], ps["wickets"]))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    insert_data()
    print("✅ Database created and populated successfully!")
