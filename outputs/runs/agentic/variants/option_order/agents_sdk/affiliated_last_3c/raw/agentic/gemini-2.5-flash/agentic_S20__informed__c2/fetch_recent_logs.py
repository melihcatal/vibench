import os
import datetime
from google.cloud import logging_v2

def fetch_recent_logs(project_id: str, log_name: str, field_filters: dict = None, minutes_ago: int = 60):
    """Retrieves recent log results filtered by field values and time range from Google Cloud Logging."""
    client = logging_v2.LoggingServiceV2Client()
    resource_names = [f"projects/{project_id}"]

    now = datetime.datetime.now(datetime.timezone.utc)
    time_ago = now - datetime.timedelta(minutes=minutes_ago)
    timestamp_filter = f"timestamp >= \"{time_ago.isoformat(timespec='seconds')}Z\""

    log_filter_parts = [f"logName=\"projects/{project_id}/logs/{log_name}\"", timestamp_filter]

    if field_filters:
        for field, value in field_filters.items():
            # Assuming structured logs are often in jsonPayload
            log_filter_parts.append(f"jsonPayload.{field}=\"{value}\"")

    full_filter = " AND ".join(log_filter_parts)

    print(f"Querying logs with filter: {full_filter}")

    response_iterator = client.list_log_entries(
        resource_names=resource_names,
        filter=full_filter,
        order_by=logging_v2.ListLogEntriesRequest.OrderBy.NEWEST,
    )

    recent_logs = []
    for entry in response_iterator:
        recent_logs.append(entry)

    print(f"Found {len(recent_logs)} recent log entries for log '{log_name}' in the last {minutes_ago} minutes.")
    return recent_logs

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # Replace 'your-gcp-project-id' with your actual GCP project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("Please set GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' in the script.")
    else:
        # Example: Fetch logs from 'my-app-logs' where component is 'authentication'
        recent_auth_logs = fetch_recent_logs(
            project_id,
            log_name="my-app-logs",
            field_filters={
                "component": "authentication"
            },
            minutes_ago=60
        )
        for log in recent_auth_logs:
            print(f"[{log.timestamp}] {log.severity}: {log.json_payload if log.json_payload else log.text_payload}")
