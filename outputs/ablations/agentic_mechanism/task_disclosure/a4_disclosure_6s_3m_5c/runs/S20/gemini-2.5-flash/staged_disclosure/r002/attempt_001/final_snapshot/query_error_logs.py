
import os
from google.cloud import logging

def query_error_logs(project_id: str, severity: str = "ERROR", time_range: str = "24h"):
    """
    Queries recent error log entries filtered by severity and time range using Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        severity: The minimum severity level to filter by (e.g., "ERROR", "WARNING", "INFO").
        time_range: The time range to query logs from (e.g., "1h", "24h", "7d").
                      This will be used to construct a timestamp filter.
    """
    client = logging.Client(project=project_id)

    # Construct the filter string
    # For more complex time range parsing, a dedicated library or more logic would be needed.
    # This example assumes simple suffixes like 'h' for hours, 'd' for days.
    # For a real application, you'd want to handle various ISO 8601 durations or specific timestamps.
    filter_string = f'severity>={severity} AND timestamp>="{time_range_to_timestamp(time_range)}"'

    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    print(f"Querying logs for project: {project_id} with severity>={severity} and time_range={time_range}")
    print("--- Log Entries ---")
    for entry in entries:
        print(f"Timestamp: {entry.timestamp}, Severity: {entry.severity}, Log Name: {entry.log_name}")
        if entry.payload:
            print(f"  Payload: {entry.payload}")
        print("-" * 20)

def time_range_to_timestamp(time_range: str) -> str:
    """
    Converts a simple time range string (e.g., "24h", "7d") to a RFC3339 timestamp string
    suitable for Google Cloud Logging filters. This is a simplified implementation.
    """
    import datetime

    now = datetime.datetime.utcnow()
    if time_range.endswith('h'):
        hours = int(time_range[:-1])
        delta = datetime.timedelta(hours=hours)
    elif time_range.endswith('d'):
        days = int(time_range[:-1])
        delta = datetime.timedelta(days=days)
    else:
        # Default to 24 hours if format is not recognized
        delta = datetime.timedelta(hours=24)

    start_time = now - delta
    return start_time.isoformat("T") + "Z" # RFC3339 format

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        query_error_logs(project_id, severity="ERROR", time_range="24h")
        # Example with different severity and time range
        # query_error_logs(project_id, severity="WARNING", time_range="1h")
