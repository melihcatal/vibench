import os
from datetime import datetime, timedelta, timezone

from google.cloud import logging_v2

from observability_client import get_query_client

def fetch_recent_logs(project_id: str, log_name: str, field: str, value: str, minutes: int = 60):
    """
    Fetches recent logs filtered by a specific JSON payload field and value.

    Args:
        project_id: The Google Cloud project ID.
        log_name: The name of the log to query.
        field: The key in the JSON payload to filter on.
        value: The value of the field to match.
        minutes: The number of minutes in the past to search.
    """
    client = get_query_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    # Construct the filter for a specific field in the JSON payload
    filter_str = (
        f'logName="projects/{project_id}/logs/{log_name}" AND '
        f'jsonPayload.{field}="{value}" AND '
        f'timestamp >= "{start_iso}" AND '
        f'timestamp <= "{end_iso}"'
    )

    print(f"Fetching recent logs with filter: {filter_str}")

    resource_names = [f"projects/{project_id}"]
    iterator = client.list_log_entries(resource_names=resource_names, filter_=filter_str)

    found_logs = []
    for entry in iterator:
        log_data = {
            "timestamp": entry.timestamp,
            "payload": entry.json_payload,
        }
        found_logs.append(log_data)
        print(f"Found matching log from {entry.timestamp}: {entry.json_payload}")

    if not found_logs:
        print("No matching logs found.")

    return found_logs

if __name__ == '__main__':
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("The GOOGLE_CLOUD_PROJECT environment variable must be set.")
    
    # Example: search for logs from a specific user in 'my-structured-log'
    fetch_recent_logs(
        gcp_project_id,
        log_name="my-structured-log",
        field="user_id",
        value="user-12345",
        minutes=1440 # 24 hours
    )
