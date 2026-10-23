"""
Queries recent error logs from Google Cloud Logging.
"""
import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client

def query_recent_error_logs():
    """
    Queries for log entries with ERROR severity in the last 24 hours.
    """
    client = get_logging_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    # Define the time range for the query
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)

    # Format timestamps for the filter
    start_iso = start_time.isoformat("T") + "Z"
    end_iso = end_time.isoformat("T") + "Z"

    # Construct the filter
    # This filter looks for logs with severity 'ERROR' within the last day.
    log_filter = (
        f'severity="ERROR" '
        f'timestamp >= "{start_iso}" AND timestamp <= "{end_iso}"'
    )

    print(f"Querying logs with filter: {log_filter}")

    # Fetch the log entries
    entries = client.list_entries(
        resource_names=[f"projects/{project_id}"],
        filter_=log_filter,
        order_by=client.DESCENDING,
        page_size=25,
    )

    # Print the results
    print("Found recent error logs:")
    for entry in entries:
        print(f"  - Timestamp: {entry.timestamp}")
        print(f"    Payload: {entry.payload}")
        if entry.resource:
            print(f"    Resource: {entry.resource.type}")

if __name__ == "__main__":
    # Note: GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT must be set
    query_recent_error_logs()
