from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone

def fetch_recent_logs(project_id: str, filter_string: str = None, duration_seconds: int = 3600):
    client = logging_v2.Client(project=project_id)

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(seconds=duration_seconds)
    timestamp_filter = f'timestamp>="{start_time.isoformat()}"'

    combined_filter = timestamp_filter
    if filter_string:
        combined_filter = f"{filter_string} AND {timestamp_filter}"

    log_entries = []
    for entry in client.list_entries(filter_=combined_filter):
        log_entries.append(entry.to_api_repr())
    return log_entries