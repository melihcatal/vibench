import os
from datetime import datetime, timedelta, timezone

from google.cloud import logging_v2

from observability_client import get_query_client

def query_error_logs(project_id: str, minutes: int = 60):
    """Queries for recent error logs in Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        minutes: The number of minutes in the past to search.
    """
    client = get_query_client()

    # Construct the filter
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    
    # Format timestamps for the filter
    start_iso = start_time.isoformat()
    end_iso = end_time.isoformat()

    filter_str = (
        f'severity="ERROR" AND '
        f'timestamp >= "{start_iso}" AND '
        f'timestamp <= "{end_iso}"'
    )

    print(f"Querying for error logs with filter: {filter_str}")

    # Make the API request
    resource_names = [f"projects/{project_id}"]
    iterator = client.list_log_entries(resource_names=resource_names, filter_=filter_str)

    results = []
    for entry in iterator:
        log_data = {
            "timestamp": entry.timestamp,
            "severity": entry.severity,
            "payload": entry.payload,
        }
        results.append(log_data)
        print(f"Found error log at {entry.timestamp}: {entry.payload}")

    if not results:
        print("No error logs found in the specified time range.")
        
    return results

if __name__ == '__main__':
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("The GOOGLE_CLOUD_PROJECT environment variable must be set.")
    
    query_error_logs(gcp_project_id, minutes=60)
