import os
from google.cloud import logging

def query_error_logs(severity: str = 'ERROR', minutes: int = 30):
    """Queries recent error log entries from Google Cloud Logging.

    Args:
        severity (str): Log severity to filter (default 'ERROR').
        minutes (int): Time range in minutes (default 30).
    """
    client = logging.Client()
    logger = client.logger('my-log')
    end_time = client.now()
    start_time = end_time - timedelta(minutes=minutes)
    query = f"logName:projects/my-project/logs/my-log severity>={severity} timestamp>={start_time} timestamp<={end_time}"
    logs = logger.list_entries(filter_=query)
    for entry in logs:
        print(entry.payload)

# Example usage
if __name__ == '__main__':
    query_error_logs()
