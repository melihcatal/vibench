import os
from google.cloud import logging

# Google Cloud Logging integration
client = logging.Client()
log_name = "projects/your-project-id/logs/app-logs"
logger = client.logger(log_name)

def fetch_recent_logs(field: str, value, minutes: int = 15):
    """Fetch recent log entries that match a field/value filter.

    Args:
        field: Field name to filter on (e.g., "correlation_id").
        value: Exact value the field must match.
        minutes: Time window to look back (default 15 minutes).

    Returns:
        List of log entries.
    """
    now = client.get_default_datetime()
    start_time = now - datetime.timedelta(minutes=minutes)
    filter_str = f"{field}={value} AND timestamp>={start_time.isoformat()}"
    return list(logger.list_entries(filter_=filter_str))

if __name__ == "__main__":
    # Example: fetch logs with a specific correlation ID
    logs = fetch_recent_logs(field="correlation_id", value="req-20230809-001")
    for log in logs:
        print(log.to_dict())
