from observability_client import get_logging_client
import datetime
import os

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

def fetch_recent_logs(log_name: str, field_filters: dict = None, time_range_minutes: int = 60):
    """Retrieves recent log results from Google Cloud Logging filtered by field values and time range.

    Args:
        log_name: The name of the log to fetch from (e.g., 'my-structured-app-log').
        field_filters: A dictionary of field names and their desired values to filter by.
                       Example: {'jsonPayload.user_id': 'user-123', 'severity': 'INFO'}
        time_range_minutes: The number of minutes back from now to query for logs.

    Returns:
        A list of dictionaries, where each dictionary is a log entry.
    """
    client = get_logging_client()

    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=time_range_minutes)

    # Base filter for time and log name
    filter_parts = [
        f'logName="projects/{PROJECT_ID}/logs/{log_name}"',
        f'timestamp >= "{start_time.isoformat()}" AND timestamp < "{now.isoformat()}"',
    ]

    # Add field filters if provided
    if field_filters:
        for field, value in field_filters.items():
            # For string values, enclose in double quotes
            if isinstance(value, str):
                filter_parts.append(f'{field}="{value}"')
            else:
                filter_parts.append(f'{field}={value}')

    filter_str = " AND ".join(filter_parts)
    print(f"Querying logs with filter: {filter_str}")

    log_entries = []
    for entry in client.list_entries(filter_=filter_str, project_ids=[PROJECT_ID]):
        log_entries.append(entry.to_api_repr())
        print(f"Found log entry: {entry.to_api_repr()}")

    return log_entries

if __name__ == '__main__':
    # Example usage: Fetch recent INFO logs for a specific user from 'my-structured-app-log'
    # Note: Replace 'my-structured-app-log' with the actual log name you're writing to.
    recent_user_logs = fetch_recent_logs(
        log_name="my-structured-app-log",
        field_filters={'jsonPayload.user_id': 'user-123', 'severity': 'INFO'},
        time_range_minutes=60
    )
    if recent_user_logs:
        print(f"Found {len(recent_user_logs)} logs for user-123.")
    else:
        print("No matching logs found.")
