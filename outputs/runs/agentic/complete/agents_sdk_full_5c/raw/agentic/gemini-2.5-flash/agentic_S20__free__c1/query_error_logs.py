from google.cloud import logging
from datetime import datetime, timedelta, timezone
import os

def query_error_logs(log_name: str, project_id: str, days_back: int = 1):
    """Queries recent error log entries from Google Cloud Logging filtered by severity and time range."""
    client = logging.Client(project=project_id)

    now = datetime.now(timezone.utc)
    # Calculate the start time for the query
    start_time = now - timedelta(days=days_back)

    # Construct the filter string. 'resource.type="global"' is a common resource type.
    # Adjust 'log_name' if you're looking for specific log streams (e.g., 'projects/YOUR_PROJECT_ID/logs/my-application-logs').
    # The filter below queries for logs with severity ERROR or higher, within the specified time range,
    # and optionally from a specific log name.
    log_filter = f"severity >= ERROR AND timestamp >= \"{start_time.isoformat()}\" AND timestamp < \"{now.isoformat()}\""
    if log_name:
        log_filter += f" AND logName=\"projects/{project_id}/logs/{log_name}\""

    print(f"Querying logs with filter: {log_filter}")

    entries = client.list_entries(filter_=log_filter, order_by=logging.DESCENDING)

    found_errors = []
    for entry in entries:
        found_errors.append(entry.to_api_repr())

    return found_errors

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name_to_query = "my-application-logs" # Replace with your log name or leave empty to query all logs
    recent_errors = query_error_logs(log_name_to_query, project_id, days_back=1)

    if recent_errors:
        print(f"Found {len(recent_errors)} error logs in the last day:")
        for i, error_log in enumerate(recent_errors):
            print(f"--- Error Log {i+1} ---")
            print(error_log)
    else:
        print("No error logs found in the last day.")
