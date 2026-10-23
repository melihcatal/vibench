
import os
from datetime import datetime, timedelta
from google.cloud import logging_v2

def query_error_logs(
    project_id: str,
    severity: str = "ERROR",
    time_range_minutes: int = 60,
):
    """
    Queries recent error log entries from Google Cloud Logging, filtered by severity and time range.

    Args:
        project_id: The Google Cloud project ID.
        severity: The minimum severity level to filter logs (e.g., "ERROR", "WARNING", "INFO").
        time_range_minutes: The number of minutes back from now to search for logs.

    Returns:
        A list of log entries.
    """
    client = logging_v2.Client(project=project_id)

    now = datetime.utcnow()
    past = now - timedelta(minutes=time_range_minutes)

    # Convert to RFC3339 format required by Logging API
    filter_start_time = past.isoformat("T") + "Z"
    filter_end_time = now.isoformat("T") + "Z"

    # Construct the filter string
    # See https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = (
        f'severity>="{severity}" '
        f'timestamp>="{filter_start_time}" '
        f'timestamp<="{filter_end_time}"'
    )

    # You might want to further refine the resource type, e.g., 'resource.type="gce_instance"'
    # or specific log names, e.g., 'logName="projects/{PROJECT_ID}/logs/your-app-log"'

    entries = client.list_entries(
        filter_=filter_string,
        order_by=logging_v2.query.DESCENDING,
    )

    log_entries = []
    for entry in entries:
        log_entries.append(entry)
    return log_entries

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID here or as an environment variable
    # For local execution, ensure you have authenticated with `gcloud auth application-default login`
    # or set the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        print(f"Querying error logs for project: {project_id}")
        recent_error_logs = query_error_logs(
            project_id=project_id,
            severity="ERROR",
            time_range_minutes=30
        )

        if recent_error_logs:
            print(f"Found {len(recent_error_logs)} recent error logs:")
            for log_entry in recent_error_logs[:5]:  # Print first 5 for brevity
                print(f"  Timestamp: {log_entry.timestamp}")
                print(f"  Severity: {log_entry.severity}")
                print(f"  Payload: {log_entry.payload}")
                print(f"  Resource: {log_entry.resource.type}, {log_entry.resource.labels}")
                print("-" * 20)
        else:
            print("No recent error logs found.")
