
from google.cloud import logging

def fetch_recent_logs(project_id: str, log_name: str, filter_string: str, hours_ago: int = 1):
    """
    Retrieves recent log entries from Google Cloud Logging, filtered by field values and time range.

    Args:
        project_id: The Google Cloud project ID.
        log_name: The name of the log to retrieve (e.g., "my-log").
        filter_string: A filter expression for log entries (e.g., "severity=ERROR").
        hours_ago: The number of hours to look back for logs.
    """
    client = logging.Client(project=project_id)

    # Calculate the time range for filtering
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    
    # Ensure now is an aware datetime object with UTC timezone
    # If now is a naive datetime, it will be treated as local time by default,
    # which can lead to issues with comparisons to UTC timestamps.
    # By ensuring it's UTC, we prevent potential timezone-related bugs.
    if now.tzinfo is None:
        now = now.replace(tzinfo=datetime.timezone.utc)
    
    start_time = now - datetime.timedelta(hours=hours_ago)
    
    # Construct the full filter string
    full_filter = f'logName="projects/{project_id}/logs/{log_name}" AND timestamp>="{start_time.isoformat()}"'
    if filter_string:
        full_filter += f' AND {filter_string}'

    print(f"Fetching logs with filter: {full_filter}")

    # List log entries
    entries = client.list_entries(filter_=full_filter)

    for entry in entries:
        print(entry.to_api_repr())

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID and log name
    YOUR_PROJECT_ID = "your-gcp-project-id"  
    YOUR_LOG_NAME = "your-log-name"          

    # Example usage: Fetch error logs from the last 2 hours
    # from a specific log
    fetch_recent_logs(
        project_id=YOUR_PROJECT_ID,
        log_name=YOUR_LOG_NAME,
        filter_string="severity=ERROR",
        hours_ago=2
    )

    # Example usage: Fetch all logs from the last 1 hour
    # from a specific log
    # fetch_recent_logs(
    #     project_id=YOUR_PROJECT_ID,
    #     log_name=YOUR_LOG_NAME,
    #     filter_string="",
    #     hours_ago=1
    # )
