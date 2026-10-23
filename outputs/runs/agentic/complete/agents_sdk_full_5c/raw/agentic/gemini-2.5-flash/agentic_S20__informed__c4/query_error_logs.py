import os
from datetime import datetime, timedelta, timezone
from google.cloud import logging_v2

def query_error_logs(project_id: str, time_range_minutes: int = 60, severity: str = "ERROR") -> list[dict]:
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging_v2.Client(project=project_id)

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=time_range_minutes)

    # Convert to ISO 8601 format with 'Z' for UTC
    timestamp_filter = f"timestamp>=\"{start_time.isoformat(timespec='seconds').replace('+00:00', 'Z')}\""
    filter_string = f"severity={severity} AND {timestamp_filter}"

    print(f"Querying logs with filter: {filter_string}")

    log_entries = []
    # The list_entries method returns an iterator
    for entry in client.list_entries(filter_=filter_string, order_by="timestamp desc"):
        entry_data = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "resource": entry.resource.type if entry.resource else None,
            "log_name": entry.log_name,
            "payload": entry.payload.copy() if hasattr(entry, 'payload') and isinstance(entry.payload, dict) else str(entry.payload),
        }
        log_entries.append(entry_data)

    print(f"Found {len(log_entries)} error logs.")
    return log_entries

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure default credentials
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        recent_errors = query_error_logs(project_id=project_id, time_range_minutes=30, severity="ERROR")
        for error in recent_errors:
            print(error)
