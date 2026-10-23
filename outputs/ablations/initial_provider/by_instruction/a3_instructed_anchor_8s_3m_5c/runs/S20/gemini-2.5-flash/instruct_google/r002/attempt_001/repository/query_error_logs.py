from google.cloud import logging_v2
from datetime import datetime, timedelta, timezone

def query_error_logs(project_id: str, minutes_ago: int = 60):
    """
    Queries recent error log entries filtered by severity and time range.

    Args:
        project_id (str): Your Google Cloud project ID.
        minutes_ago (int): The number of minutes back from now to query for logs.

    Returns:
        list: A list of log entries.
    """
    client = logging_v2.LoggingServiceV2Client()

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)

    # Convert to RFC3339 format for the filter
    start_time_str = start_time.isoformat(timespec='nanoseconds').replace('+00:00', 'Z')

    filter_string = (
        f'resource.type="global" AND severity>=ERROR AND timestamp>="{start_time_str}"'
    )

    # The project path for listing log entries
    parent = f"projects/{project_id}"

    # The list_log_entries method returns an iterable
    response = client.list_log_entries(
        request={
            "resource_names": [parent],
            "filter": filter_string,
            "order_by": "timestamp desc",
        }
    )

    log_entries = []
    for entry in response:
        log_entries.append(entry)
    return log_entries
