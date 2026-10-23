from google.cloud import logging_v2
from datetime import datetime, timezone

def fetch_recent_logs(project_id: str, filter_string: str = "", start_time: datetime = None, end_time: datetime = None):
    """
    Retrieves recent log results from Google Cloud Logging, filtered by field values and time range.

    Args:
        project_id: The Google Cloud project ID.
        filter_string: An optional filter string to apply to the log entries.
                       See https://cloud.google.com/logging/docs/view/logging-query-language for syntax.
        start_time: Optional datetime object specifying the start of the time range (UTC).
        end_time: Optional datetime object specifying the end of the time range (UTC).

    Returns:
        A list of log entry dictionaries.
    """
    client = logging_v2.client.Client(project=project_id)

    resource_names = [f"projects/{project_id}"]

    full_filter = filter_string
    if start_time:
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        full_filter += f" timestamp>=\"{start_time.isoformat()}\""
    if end_time:
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        full_filter += f" timestamp<=\"{end_time.isoformat()}\""

    entries = client.list_entries(resource_names=resource_names, filter_=full_filter)

    log_entries = []
    for entry in entries:
        log_entries.append(entry.to_dict())
    return log_entries
