# API Performance Monitor

## Project Overview

API Performance Monitor is a Python-based application that tracks API performance metrics such as response time and status codes.

## Features

* Monitor API response times
* Track API status codes
* Store logs in SQLite database
* Display monitoring data using Flask dashboard
* Calculate average response time
* Count total API requests

## Technologies Used

* Python
* Flask
* Requests
* SQLite

## Project Structure

API-Monitor/
│
── app.py
── monitor.py
── database.py
── api_monitor.db
── README.md

## How to Run

### 1. Create Virtual Environment

python -m venv venv

### 2. Activate Environment

Windows:

venv\Scripts\activate

### 3. Install Dependencies

pip install flask requests

### 4. Create Database

python database.py

### 5. Start Monitoring

python monitor.py

### 6. Run Dashboard

python app.py

### 7. Open Browser

http://127.0.0.1:5000

## Output

* API Response Time Monitoring
* Status Code Tracking
* Performance Dashboard

## Author

Navin Pradhan
