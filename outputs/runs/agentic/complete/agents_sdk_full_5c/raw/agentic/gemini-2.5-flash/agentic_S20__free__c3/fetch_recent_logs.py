import os
from datetime import datetime, timedelta
from google.cloud import logging_v2
from google.cloud.logging_v2.client import LoggingServiceV2Client

def fetch_recent_logs(project_id: str, log_name: str, field_filter: dict = None, minutes_back: int = 60, limit: int = 5):
    """Retrieves recent log entries filtered by log name, field values, and time range from Google Cloud Logging.

    Args:
        project_id: Your Google Cloud project ID.
        log_name: The short name of the log (e.g., 'my-app-logs').
        field_filter: A dictionary of field-value pairs to filter by (e.g., {'jsonPayload.user_id': 'user123'}).
        minutes_back: Number of minutes to look back for logs.
        limit: Maximum number of log entries to fetch.
    """
    client: LoggingServiceV2Client = logging_v2.LoggingServiceV2Client()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=minutes_back)

    # Convert to RFC3339 format
    start_time_str = start_time.isoformat("T") + "Z"

    # Build the filter string
    filter_parts = [
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp >= "{start_time_str}"'
    ]

    if field_filter:
        for key, value in field_filter.items():
            if isinstance(value, str):
                filter_parts.append(f'{key}="{value}"')
            else:
                filter_parts.append(f'{key}={value}')

    filter_string = " AND ".join(filter_parts)

    print(f"Fetching recent logs for project {project_id} with filter: {filter_string}")
    response_iterator = client.list_log_entries(
        resource_names=[f"projects/{project_id}"],
        filter=filter_string,
        order_by="timestamp desc",
        page_size=limit
    )

    found_logs = False
    for entry in response_iterator:
        found_logs = True
        print("---------------------------------------------------")
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        print(f"Log Name: {entry.log_name}")
        if entry.json_payload:
            print(f"JSON Payload: {entry.json_payload}")
        elif entry.text_payload:
            print(f"Text Payload: {entry.text_payload}")
        print("---------------------------------------------------")
    
    if not found_logs:
        print("No logs found for the given criteria.")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print("\n--- Fetching general app logs ---")
        fetch_recent_logs(
            project_id=project_id,
            log_name="my-app-logs",
            minutes_back=120, # Last 2 hours
            limit=3
        )
        
        print("\n--- Fetching logs for a specific user ---")
        fetch_recent_logs(
            project_id=project_id,
            log_name="my-app-logs",
            field_filter={"jsonPayload.user_id": "user123"},
            minutes_back=60,
            limit=2
        )
        
        print("\n--- Fetching logs for a specific request ID ---")
        # Note: 'request_id' is directly in jsonPayload, not trace for list_log_entries filtering
        # If using `trace` for filtering, it would be different. Here we assume `request_id` is in `jsonPayload`.
        fetch_recent_logs(
            project_id=project_id,
            log_name="my-app-request-logs",
            field_filter={"jsonPayload.request_id": "custom-req-abc-123"},
            minutes_back=60,
            limit=2
        )

    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
