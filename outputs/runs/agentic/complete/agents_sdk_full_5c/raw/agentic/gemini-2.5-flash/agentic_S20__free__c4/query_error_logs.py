from google.cloud import logging
import os
from datetime import datetime, timedelta, timezone

def query_error_logs(log_name: str, days_back: int = 1):
    """
    Queries recent error log entries filtered by severity and time range in Google Cloud Logging.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = logging.Client(project=project_id)

    # Calculate time range for the query
    now = datetime.now(timezone.utc)
    n_days_ago = now - timedelta(days=days_back)

    # Construct the filter string
    # Example: resource.type="global" AND severity>="ERROR" AND timestamp>="2023-10-26T00:00:00Z"
    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" '  # Target specific log
        f'AND severity>="ERROR" '  # Filter by error severity or higher
        f'AND timestamp>="{n_days_ago.isoformat(timespec="seconds")}"'
    )

    print(f"Querying logs with filter: {filter_string}")

    # Execute the query
    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    found_errors = []
    for entry in entries:
        # Convert LogEntry object to a dictionary for easier printing/handling
        entry_dict = entry.to_api_repr()
        found_errors.append(entry_dict)
        print(f"Found Error [{entry.severity}]: {entry.timestamp} {entry.payload}")

    return found_errors

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var and auth)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    error_logs = query_error_logs("my-app-logs", days_back=0) # Query for today's errors
    print(f"\nTotal error logs found: {len(error_logs)}")
