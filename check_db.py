from database import fetch_recent_logs

for row in fetch_recent_logs(limit=100):
    print(dict(row))