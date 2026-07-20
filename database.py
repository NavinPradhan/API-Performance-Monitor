import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("DB_PATH", Path(__file__).resolve().parent / "api_monitor.db"))


def get_connection(db_path=None):
    db_path = db_path or DB_PATH
    connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 30000")
    return connection


def initialize_database(db_path=None):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                response_time REAL,
                status_code INTEGER,
                url TEXT
            )
            """
        )

        columns = {row[1] for row in cursor.execute("PRAGMA table_info(api_logs)").fetchall()}
        if "timestamp" not in columns:
            cursor.execute("ALTER TABLE api_logs ADD COLUMN timestamp TEXT DEFAULT CURRENT_TIMESTAMP")
        if "url" not in columns:
            cursor.execute("ALTER TABLE api_logs ADD COLUMN url TEXT")

        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_api_logs_timestamp ON api_logs (timestamp DESC)"
        )
        conn.commit()


def insert_api_log(response_time, status_code, url, db_path=None):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO api_logs (response_time, status_code, url)
            VALUES (?, ?, ?)
            """,
            (response_time, status_code, url),
        )
        conn.commit()


def fetch_recent_logs(limit=100, db_path=None):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, timestamp, response_time, status_code, url
            FROM api_logs
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        )
        return cursor.fetchall()


def fetch_summary(db_path=None):
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) AS total_requests, AVG(response_time) AS average_response_time FROM api_logs"
        )
        row = cursor.fetchone()
        return {
            "total_requests": row["total_requests"] or 0,
            "average_response_time": round(row["average_response_time"], 2)
            if row["average_response_time"] is not None
            else 0.0,
        }


if __name__ == "__main__":
    initialize_database()
    print("Database created successfully at", DB_PATH)