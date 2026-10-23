import os
from google.cloud import logging

client = logging.Client()
logger = client.logger("recent-logs")


def fetch_recent_logs():
    query_client = client.query(filter_='timestamp > "2026-01-01T00:00:00Z"')
    for entry in query_client.run():
        print(entry.payload)


if __name__ == "__main__":
    fetch_recent_logs()
