from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_project_id

def query_recent_errors(time_window_minutes: int = 60):
    """
    Queries for ERROR-level logs in the last N minutes from Google Cloud Logging.

    Args:
        time_window_minutes: The number of minutes to look back.
    """
    client = logging_v2.services.logging_service_v2.LoggingServiceV2Client()
    project_id = get_gcp_project_id()
    
    # Construct the filter
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=time_window_minutes)
    
    # Format times for the API
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Filter for severity and timestamp
    filter_str = (
        f'severity="ERROR" AND '
        f'timestamp >= "{start_time_str}" AND '
        f'timestamp <= "{end_time_str}"'
    )
    
    resource_names = [f"projects/{project_id}"]

    print(f"Querying for error logs with filter: {filter_str}")

    # Make the API request
    entries = client.list_log_entries(
        resource_names=resource_names,
        filter_=filter_str,
        page_size=10,
    )

    # Process and print results
    print("Found recent error logs:")
    for entry in entries:
        print(f"  - Time: {entry.timestamp}, Payload: {entry.json_payload}")

if __name__ == "__main__":
    query_recent_errors()
