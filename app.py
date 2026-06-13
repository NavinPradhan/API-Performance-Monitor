from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():

    conn = sqlite3.connect("api_monitor.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM api_logs")
    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM api_logs")
    total_requests = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(response_time) FROM api_logs")
    avg_time = cursor.fetchone()[0]

    conn.close()

    html = f"""
    <h1>API Performance Monitor</h1>

    <h3>Total Requests: {total_requests}</h3>
    <h3>Average Response Time: {round(avg_time, 2)} sec</h3>

    <table border='1'>
    <tr>
        <th>ID</th>
        <th>Response Time</th>
        <th>Status Code</th>
    </tr>
    """

    for row in rows:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
        </tr>
        """

    html += "</table>"

    return html

if __name__ == "__main__":
    app.run(debug=True)