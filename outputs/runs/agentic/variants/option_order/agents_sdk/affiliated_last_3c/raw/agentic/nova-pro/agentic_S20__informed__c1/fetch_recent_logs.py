import os
from google.cloud import logging

client = logging.Client()

def fetch_recent_logs():
    query_client = client.logging_query_client
    query = 'severity=INFO'
    time_range = '2023-01-01T00:00:00Z, 2023-12-31T23:59:59Z'
    results = query_client.query(query, time_range)
    for entry in results:
        print(entry)
fetch_recent_logs()