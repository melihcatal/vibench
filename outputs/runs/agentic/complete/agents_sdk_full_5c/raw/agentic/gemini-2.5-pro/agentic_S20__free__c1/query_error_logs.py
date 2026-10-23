from datetime import datetime, timedelta, timezone
from google.cloud.logging_v2.client import Client as LoggingClient

def query_recent_error_logs(project_id: str):
    """
    Queries for recent log entries with 'ERROR' severity in Google Cloud Logging.

    Args:
        project_id: Your Google Cloud project ID.
    
    Returns:
        A list of log entries matching the query.
    """
    client = LoggingClient()

    # Define the time range (last 24 hours)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    
    # Format timestamps for the filter
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Construct a filter for ERROR severity within the time range
    filter_str = (
        f'severity="ERROR" '
        f'AND timestamp >= "{start_time_str}" '
        f'AND timestamp <= "{end_time_str}"'
    )

    print(f"Using filter: {filter_str}")

    # List log entries
    entries = client.list_log_entries(
        resource_names=[f"projects/{project_id}"],
        filter_=filter_str,
        page_size=100,
    )
    
    error_logs = list(entries)
    print(f"Found {len(error_logs)} error log entries.")
    return error_logs

# Example usage:
# import os
# project_id = os.environ.get("GCP_PROJECT_ID")
# if project_id:
#     recent_errors = query_recent_error_logs(project_id)
#     for entry in recent_errors:
#         print(entry.payload)
