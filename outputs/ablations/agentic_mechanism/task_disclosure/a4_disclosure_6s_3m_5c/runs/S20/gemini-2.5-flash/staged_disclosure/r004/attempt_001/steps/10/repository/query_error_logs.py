from google.cloud import logging_v2
import datetime

def query_error_logs(project_id: str, severity: str, time_range_seconds: int):
    """
    Queries recent error log entries from Google Cloud Logging, filtered by severity and time range.

    Args:
        project_id: Your Google Cloud Project ID.
        severity: The minimum severity of log entries to retrieve (e.g., "ERROR", "WARNING", "INFO").
        time_range_seconds: The time range in seconds to look back for log entries.
    """
    client = logging_v2.Client(project=project_id)

    now = datetime.datetime.now(datetime.timezone.utc)
    time_cutoff = now - datetime.timedelta(seconds=time_range_seconds)
    timestamp_filter = f'timestamp >= "{time_cutoff.isoformat()}"'

    log_filter = f'severity >= {severity} AND {timestamp_filter}'

    print(f"Querying logs for project: {project_id} with filter: {log_filter}")

    entries = client.list_entries(filter_=log_filter, order_by=logging_v2.DESCENDING)

    for entry in entries:
        print(f"Log Entry: {entry.json_payload or entry.text_payload or entry.proto_payload} (Severity: {entry.severity}, Timestamp: {entry.timestamp})")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id"
    
    # Example usage: Query ERROR logs from the last hour (3600 seconds)
    query_error_logs(YOUR_PROJECT_ID, "ERROR", 3600)
