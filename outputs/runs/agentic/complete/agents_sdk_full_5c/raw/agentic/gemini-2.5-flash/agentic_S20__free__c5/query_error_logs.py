from observability_client import get_logging_client
import datetime
import os

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

def query_error_logs(time_range_minutes: int = 60):
    """Queries recent error log entries filtered by severity and time range in Google Cloud Logging.

    Args:
        time_range_minutes: The number of minutes back from now to query for logs.

    Returns:
        A list of dictionaries, where each dictionary is a log entry.
    """
    client = get_logging_client()

    # Calculate the time boundary
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # Using resource.type="global" to catch various logs, or specify "gae_app", "k8s_container", etc.
    # For structured logs, severity is often a top-level field.
    # For older log formats, it might be textPayload or jsonPayload.severity.
    # Assuming structured logs with top-level severity and textPayload for older ones.
    filter_str = f'''
        severity >= "ERROR"
        timestamp >= "{start_time.isoformat()}" AND timestamp < "{now.isoformat()}"
    '''
    # Remove extra spaces and newlines from filter_str
    filter_str = " ".join(filter_str.split())

    print(f"Querying logs with filter: {filter_str}")

    log_entries = []
    # The list_entries method returns an iterator
    for entry in client.list_entries(filter_=filter_str, project_ids=[PROJECT_ID]):
        log_entries.append(entry.to_api_repr())
        print(f"Found error log: {entry.to_api_repr()}")

    return log_entries

if __name__ == '__main__':
    # Example usage: Query error logs from the last 30 minutes
    recent_errors = query_error_logs(time_range_minutes=30)
    if recent_errors:
        print(f"Found {len(recent_errors)} error logs.")
    else:
        print("No error logs found in the last 30 minutes.")
