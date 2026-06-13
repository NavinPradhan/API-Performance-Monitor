import sqlite3

conn = sqlite3.connect("api_monitor.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS api_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    response_time REAL,
    status_code INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")