import os
from datetime import datetime, timedelta, timezone
from google.cloud import logging

def query_error_logs(
    project_id: str = None,
    log_name: str = None,
    time_range_minutes: int = 60,
    severity: str = "ERROR"
):
    """
    Queries recent error log entries filtered by severity and time range from Google Cloud Logging.
    """
    client = logging.Client(project=project_id)

    now = datetime.now(timezone.utc)
    # Define start_time in RFC3339 format
    start_time = (now - timedelta(minutes=time_range_minutes)).isoformat(timespec='seconds') + 'Z'

    # Build the filter string
    filters = [f'severity>="{severity}"']
    filters.append(f'timestamp>="{start_time}"')
    if log_name:
        filters.append(f'logName="projects/{client.project}/logs/{log_name}"')

    filter_string = " ".join(filters)
    print(f"Querying logs with filter: {filter_string}")

    # Iterate over log entries
    for entry in client.list_entries(filter_=filter_string, order_by=logging.DESCENDING):
        print(f"Timestamp: {entry.timestamp}, Severity: {entry.severity}, LogName: {entry.log_name}, Payload: {entry.payload}")

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set or gcloud is authenticated.
    # Replace with your actual Google Cloud Project ID
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    query_error_logs(
        project_id=project_id,
        log_name="my-application-logs", # Optional: specify a log name
        time_range_minutes=30,
        severity="ERROR"
    )
