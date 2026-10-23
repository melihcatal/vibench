from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone

def fetch_recent_logs(project_id: str, log_filter: str, minutes_ago: int = 60):
    """
    Retrieves recent log results filtered by field values and time range.

    Args:
        project_id (str): Your Google Cloud project ID.
        log_filter (str): The filter string to apply to the log entries (e.g., 'jsonPayload.user="test_user"').
        minutes_ago (int): The number of minutes back from now to query for logs.

    Returns:
        list: A list of log entries.
    """
    client = logging_v2.LoggingServiceV2Client()

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    # Convert to RFC3339 format for the filter
    start_time_str = start_time.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')

    full_filter_string = f'{log_filter} AND timestamp>="{start_time_str}'

    # The project path for listing log entries
    parent = f"projects/{project_id}"

    # The list_log_entries method returns an iterable
    response = client.list_log_entries(
        request={
            "resource_names": [parent],
            "filter": full_filter_string,
            "order_by": "timestamp desc",
        }
    )

    log_entries = []
    for entry in response:
        log_entries.append(entry)
    return log_entries
