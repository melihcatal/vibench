import os
from datetime import datetime, timedelta, timezone
import google.cloud.logging_v2

# Google Cloud project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def query_error_logs(project_id: str, minutes_ago: int = 60):
    """
    Queries recent error log entries filtered by severity and time range in Google Cloud Logging.
    """
    if not project_id:
        raise ValueError("Google Cloud project ID must be provided.")

    client = google.cloud.logging_v2.LoggingServiceV2Client()
    project_path = f"projects/{project_id}"

    now = datetime.now(timezone.utc)
    # Calculate the timestamp for `minutes_ago` from now
    timestamp_cutoff = now - timedelta(minutes=minutes_ago)

    # Construct the filter string
    # https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = f"severity >= ERROR AND timestamp >= \"{timestamp_cutoff.isoformat(timespec='nanoseconds')}\"

    print(f"Querying for error logs in project {project_id} from the last {minutes_ago} minutes...")
    print(f"Filter: {filter_string}")

    # List log entries
    response = client.list_log_entries(
        resource_names=[project_path],
        filter=filter_string,
        order_by="timestamp desc"
    )

    found_errors = []
    for entry in response.entries:
        found_errors.append(entry)
        print(f"  [{entry.severity}] {entry.timestamp}: {entry.payload}")

    print(f"Found {len(found_errors)} error log entries.")
    return found_errors

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable
    if PROJECT_ID:
        query_error_logs(project_id=PROJECT_ID, minutes_ago=30)
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
