import os
import datetime
from google.cloud import logging_v2

def query_error_logs(project_id: str, minutes_ago: int = 60):
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project_id}"]

    now = datetime.datetime.now(datetime.timezone.utc)
    time_ago = now - datetime.timedelta(minutes=minutes_ago)
    timestamp_filter = f"timestamp >= \"{time_ago.isoformat(timespec='seconds')}Z\""

    # Filter for ERROR or higher severity
    log_filter = f"severity >= ERROR AND {timestamp_filter}"

    print(f"Querying logs with filter: {log_filter}")

    response_iterator = client.list_log_entries(
        resource_names=resource_names,
        filter=log_filter,
        order_by=logging_v2.ListLogEntriesRequest.OrderBy.NEWEST,
    )

    error_logs = []
    for entry in response_iterator:
        error_logs.append(entry)
    
    print(f"Found {len(error_logs)} error log entries in the last {minutes_ago} minutes.")
    return error_logs

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Replace 'your-gcp-project-id' with your actual GCP project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("Please set GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' in the script.")
    else:
        recent_errors = query_error_logs(project_id, minutes_ago=30)
        for log in recent_errors:
            print(f"[{log.timestamp}] {log.severity}: {log.json_payload if log.json_payload else log.text_payload}")
