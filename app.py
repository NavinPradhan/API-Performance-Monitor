import os

from flask import Flask, render_template

from database import fetch_recent_logs, fetch_summary, initialize_database

app = Flask(__name__, template_folder="templates")

initialize_database()


@app.route("/")
def home():
    summary = fetch_summary()
    rows = fetch_recent_logs(limit=100)
    return render_template("dashboard.html", summary=summary, rows=rows)


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "5000")), debug=False)