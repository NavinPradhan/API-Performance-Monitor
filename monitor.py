import requests
import time
import sqlite3

while True:

    start = time.time()

    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts"
    )

    end = time.time()

    response_time = round(end - start, 2)

    print("Response Time:", response_time)
    print("Status Code:", response.status_code)

    conn = sqlite3.connect("api_monitor.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO api_logs
        (response_time, status_code)
        VALUES (?, ?)
        """,
        (response_time, response.status_code)
    )

    conn.commit()
    conn.close()

    print("Data Saved")
    print("----------------")

    time.sleep(10)