import os
from datetime import datetime, timedelta, timezone
import google.cloud.logging_v2

# Google Cloud project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def fetch_recent_logs(project_id: str, log_name: str, field_name: str, field_value: str, minutes_ago: int = 60):
    """
    Retrieves recent log results filtered by log name, field values, and time range
    in Google Cloud Logging.
    """
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided.")

    client = google.cloud.logging_v2.LoggingServiceV2Client()
    project_path = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    timestamp_cutoff = now - timedelta(minutes=minutes_ago)

    # Construct the filter string
    # https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = (
        f"logName=\"projects/{project_id}/logs/{log_name}\" AND "
        f"{field_name}=\"{field_value}\" AND "
        f"timestamp >= \"{timestamp_cutoff.isoformat(timespec='nanoseconds')}\"
    )

    print(f"Fetching recent logs in project {project_id} for log '{log_name}' with {field_name}='{field_value}' from the last {minutes_ago} minutes...")
    print(f"Filter: {filter_string}")

    response = client.list_log_entries(
        resource_names=[project_path],
        filter=filter_string,
        order_by="timestamp desc"
    )

    found_logs = []
    for entry in response.entries:
        found_logs.append(entry)
        print(f"  [{entry.severity}] {entry.timestamp}: {entry.payload}")

    print(f"Found {len(found_logs)} log entries.")
    return found_logs

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable
    if PROJECT_ID:
        fetch_recent_logs(
            project_id=PROJECT_ID,
            log_name="my-app-logs",  # Use a log name that exists in your project
            field_name="jsonPayload.event_type", # Or a different field, e.g., 'jsonPayload.user_id'
            field_value="authentication",
            minutes_ago=60
        )
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
