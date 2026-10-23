from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone
import os

def query_error_logs(project_id: str, time_range_minutes: int = 60):
    """Queries recent error log entries filtered by severity and time range from Google Cloud Logging."""
    client = logging_v2.Client(project=project_id)

    now = datetime.now(timezone.utc)
    # Start time for the query (e.g., last 60 minutes)
    start_time = now - timedelta(minutes=time_range_minutes)

    # Convert to RFC3339 format
    start_time_str = start_time.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')
    end_time_str = now.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')

    # Construct the filter string
    # Note: severity can be ERROR, WARNING, INFO, DEBUG, etc.
    # For this function, we specifically target ERROR severity.
    filter_str = f'severity=("ERROR" OR "CRITICAL" OR "ALERT" OR "EMERGENCY") AND timestamp >= "{start_time_str}" AND timestamp <= "{end_time_str}"'
    
    print(f"Querying logs for project '{project_id}' with filter: {filter_str}")

    entries_found = 0
    for entry in client.list_entries(order_by=logging_v2.LogEntryOrder.NEWEST,
                                     filter_=filter_str):
        entries_found += 1
        print(f"Timestamp: {entry.timestamp}")
        print(f"Severity: {entry.severity}")
        print(f"Log Name: {entry.log_name}")
        if entry.payload: # Check if payload is not None
            if entry.json_payload:
                print(f"Payload: {entry.json_payload}")
            elif entry.text_payload:
                print(f"Payload: {entry.text_payload}")
            elif entry.proto_payload:
                print(f"Payload: {entry.proto_payload}")
        print("---")
    
    if entries_found == 0:
        print("No error logs found in the specified time range.")
    else:
        print(f"Total {entries_found} error logs found.")

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    # Example usage: Query error logs from the last 30 minutes
    query_error_logs(project_id=project_id, time_range_minutes=30)
