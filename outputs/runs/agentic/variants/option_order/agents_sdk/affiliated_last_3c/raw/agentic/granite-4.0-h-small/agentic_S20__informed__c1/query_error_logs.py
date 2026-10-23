import os
from google.cloud import logging

# Google Cloud Logging integration
client = logging.Client()
log_name = "projects/your-project-id/logs/app-logs"
logger = client.logger(log_name)

def query_error_logs(severity: str = "ERROR", minutes: int = 30):
    """Query recent error logs using Google Cloud Logging.

    Returns a list of log entries matching the given severity and time range.
    """
    now = client.get_default_datetime()
    start_time = now - datetime.timedelta(minutes=minutes)
    # Construct a filter string
    filter_str = f"severity={severity} AND timestamp>={start_time.isoformat()}"
    entries = logger.list_entries(filter_=filter_str)
    return list(entries)

if __name__ == "__main__":
    # Example usage
    for entry in query_error_logs(severity="ERROR", minutes=60):
        print(entry.to_dict())
