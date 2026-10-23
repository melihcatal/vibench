import os
from datetime import datetime, timedelta, timezone
from google.cloud import logging

def fetch_recent_logs(
    project_id: str = None,
    log_name: str = None,
    time_range_minutes: int = 60,
    field_filters: dict = None
):
    """
    Retrieves recent log results filtered by field values and time range from Google Cloud Logging.
    """
    client = logging.Client(project=project_id)

    now = datetime.now(timezone.utc)
    start_time = (now - timedelta(minutes=time_range_minutes)).isoformat(timespec='seconds') + 'Z'

    filters = [f'timestamp>="{start_time}"']
    if log_name:
        filters.append(f'logName="projects/{client.project}/logs/{log_name}"')

    if field_filters:
        for field, value in field_filters.items():
            # For structured logs, fields are usually nested under `jsonPayload` or `textPayload`
            # This example assumes `jsonPayload` fields.
            filters.append(f'jsonPayload.{field}="{value}"')

    filter_string = " ".join(filters)
    print(f"Fetching logs with filter: {filter_string}")

    # Iterate over log entries
    for entry in client.list_entries(filter_=filter_string, order_by=logging.DESCENDING):
        print(f"Timestamp: {entry.timestamp}, Severity: {entry.severity}, LogName: {entry.log_name}, Payload: {entry.payload}")

if __name__ == "__main__":
    # Example usage:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    fetch_recent_logs(
        project_id=project_id,
        log_name="my-application-logs",
        time_range_minutes=60,
        field_filters={"user_id": "user-123"} # Filter for specific user_id
    )
    print("\n--- Fetching all recent logs from specific log name ---")
    fetch_recent_logs(
        project_id=project_id,
        log_name="my-application-logs",
        time_range_minutes=10,
        field_filters={}
    )
