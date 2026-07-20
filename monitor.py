import logging
import os
import signal
import sys
import time

import requests

from database import initialize_database, insert_api_log

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "10"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
BASE_BACKOFF_DELAY = float(os.getenv("BASE_BACKOFF_DELAY", "1.0"))
MAX_BACKOFF_DELAY = float(os.getenv("MAX_BACKOFF_DELAY", "30.0"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SHOULD_STOP = {"value": False}


def signal_handler(signum, _frame):
    logger.info("Received signal %s; shutting down monitor", signum)
    SHOULD_STOP["value"] = True


for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, signal_handler)


def calculate_backoff_delay(attempt, base_delay=BASE_BACKOFF_DELAY, max_delay=MAX_BACKOFF_DELAY):
    if attempt <= 0:
        return base_delay
    return min(base_delay * (2**attempt), max_delay)


def log_result(response_time, status_code):
    logger.info("URL=%s status=%s response_time=%.2f sec", API_URL, status_code, response_time)


def monitor_loop():
    initialize_database()
    session = requests.Session()
    consecutive_failures = 0

    try:
        while not SHOULD_STOP["value"]:
            start = time.monotonic()
            status_code = 0

            try:
                response = session.get(API_URL, timeout=REQUEST_TIMEOUT)
                status_code = response.status_code
                response.raise_for_status()
            except requests.RequestException as exc:
                response_time = round(time.monotonic() - start, 2)
                logger.warning("Request failed for %s: %s", API_URL, exc)
                logger.info("Response Time: %.2f sec", response_time)
                try:
                    insert_api_log(response_time, status_code, API_URL)
                except Exception as db_exc:  # pragma: no cover - defensive logging
                    logger.error("Failed to write log entry: %s", db_exc)

                consecutive_failures += 1
                backoff_delay = calculate_backoff_delay(
                    consecutive_failures,
                    base_delay=BASE_BACKOFF_DELAY,
                    max_delay=MAX_BACKOFF_DELAY,
                )
                logger.info("Retrying in %.2f seconds", backoff_delay)
                time.sleep(backoff_delay)
                continue

            response_time = round(time.monotonic() - start, 2)
            log_result(response_time, status_code)
            try:
                insert_api_log(response_time, status_code, API_URL)
            except Exception as db_exc:  # pragma: no cover - defensive logging
                logger.error("Failed to write log entry: %s", db_exc)

            consecutive_failures = 0
            if not SHOULD_STOP["value"]:
                time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    finally:
        session.close()


if __name__ == "__main__":
    try:
        monitor_loop()
    except KeyboardInterrupt:
        logger.info("Exiting monitor")
        sys.exit(0)