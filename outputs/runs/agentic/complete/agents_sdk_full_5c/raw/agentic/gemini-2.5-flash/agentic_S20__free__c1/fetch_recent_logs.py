from google.cloud import logging
from datetime import datetime, timedelta, timezone
import os

def fetch_recent_logs(log_name: str, project_id: str, field_filters: dict = None, days_back: int = 1):
    """Retrieves recent log results from Google Cloud Logging filtered by field values and time range."""
    client = logging.Client(project=project_id)

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=days_back)

    # Base filter for time range
    log_filter = f"timestamp >= \"{start_time.isoformat()}\" AND timestamp < \"{now.isoformat()}\""

    # Add log name filter if provided
    if log_name:
        log_filter += f" AND logName=\"projects/{project_id}/logs/{log_name}\""

    # Add additional field filters
    if field_filters:
        for field, value in field_filters.items():
            # For string values, use quotes; for numbers/booleans, no quotes.
            # This example assumes basic string or exact match filtering.
            # More complex filters might require specific handling for operators (>, <, etc.)
            if isinstance(value, str):
                log_filter += f" AND jsonPayload.{field}=\"{value}\"" 
            else:
                log_filter += f" AND jsonPayload.{field}={value}"
    
    print(f"Querying logs with filter: {log_filter}")

    entries = client.list_entries(filter_=log_filter, order_by=logging.DESCENDING)

    found_logs = []
    for entry in entries:
        found_logs.append(entry.to_api_repr())

    return found_logs

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name_to_query = "my-application-logs" # Replace with your log name

    # Example: fetch logs with event_type 'user_login' and status 'failure'
    custom_filters = {
        "event_type": "user_login",
        "status": "failure"
    }

    recent_filtered_logs = fetch_recent_logs(log_name_to_query, project_id, field_filters=custom_filters, days_back=7)

    if recent_filtered_logs:
        print(f"Found {len(recent_filtered_logs)} filtered logs in the last 7 days:")
        for i, log_entry in enumerate(recent_filtered_logs):
            print(f"--- Log Entry {i+1} ---")
            print(log_entry)
    else:
        print("No filtered logs found.")
