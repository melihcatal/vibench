from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_project_id

def fetch_logs_by_field(user_id: str, time_window_hours: int = 24):
    """
    Fetches recent logs from Google Cloud Logging filtered by a JSON payload field.

    Args:
        user_id: The user ID to filter logs for.
        time_window_hours: The number of hours to look back.
    """
    client = logging_v2.services.logging_service_v2.LoggingServiceV2Client()
    project_id = get_gcp_project_id()

    # Calculate time window
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=time_window_hours)
    start_time_str = start_time.isoformat("T") + "Z"

    # Construct a filter to find logs for a specific user
    filter_str = (
        f'jsonPayload.user_id="{user_id}" AND '
        f'timestamp >= "{start_time_str}"'
    )

    resource_names = [f"projects/{project_id}"]
    
    print(f"Fetching logs with filter: {filter_str}")

    # Make the API request
    log_entries = client.list_log_entries(
        resource_names=resource_names,
        filter_=filter_str,
        order_by="timestamp desc",
        page_size=25
    )

    # Print the results
    print(f"Found logs for user '{user_id}':")
    for entry in log_entries:
        print(
            f"  - Timestamp: {entry.timestamp}, "
            f"Message: {entry.json_payload.get('message', 'N/A')}"
        )

if __name__ == "__main__":
    # Example: fetch logs for a specific user
    fetch_logs_by_field(user_id="user-12345")
