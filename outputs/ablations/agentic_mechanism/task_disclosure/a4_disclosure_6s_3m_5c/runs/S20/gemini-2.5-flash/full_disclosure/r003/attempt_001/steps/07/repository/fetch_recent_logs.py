from google.cloud import logging_v2
from datetime import datetime, timedelta

def fetch_recent_logs(project_id: str, filter_string: str = None, hours_ago: int = 1):
    """
    Retrieves recent log results from Google Cloud Logging, filtered by field values and time range.

    Args:
        project_id: The Google Cloud project ID.
        filter_string: Optional filter string for log entries (e.g., 'resource.type="cloud_run_revision" AND severity=ERROR').
        hours_ago: The number of hours back from now to fetch logs.
    
    Returns:
        A list of log entries.
    """
    client = logging_v2.Client(project=project_id)

    now = datetime.utcnow()
    start_time = now - timedelta(hours=hours_ago)
    
    time_filter = f'timestamp>="{start_time.isoformat("T")}Z"'
    
    full_filter = time_filter
    if filter_string:
        full_filter = f"{filter_filter} AND {filter_string}"

    entries = list(client.list_entries(
        filter_=full_filter,
        order_by=logging_v2.DESCENDING
    ))
    
    return entries

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    YOUR_PROJECT_ID = "your-gcp-project-id" 

    # Example usage: Fetch all logs from the last 2 hours
    print(f"Fetching all logs from the last 2 hours for project {YOUR_PROJECT_ID}...")
    all_recent_logs = fetch_recent_logs(YOUR_PROJECT_ID, hours_ago=2)
    for entry in all_recent_logs[:5]: # Print first 5 entries
        print(f"Entry: {entry.payload}, Severity: {entry.severity}")
    print(f"Total logs fetched: {len(all_recent_logs)}")

    print("\nFetching error logs from Cloud Run in the last 1 hour...")
    cloud_run_error_filter = 'resource.type="cloud_run_revision" AND severity=ERROR'
    cloud_run_error_logs = fetch_recent_logs(YOUR_PROJECT_ID, filter_string=cloud_run_error_filter, hours_ago=1)
    for entry in cloud_run_error_logs[:5]: # Print first 5 entries
        print(f"Entry: {entry.payload}, Severity: {entry.severity}")
    print(f"Total Cloud Run error logs fetched: {len(cloud_run_error_logs)}")
