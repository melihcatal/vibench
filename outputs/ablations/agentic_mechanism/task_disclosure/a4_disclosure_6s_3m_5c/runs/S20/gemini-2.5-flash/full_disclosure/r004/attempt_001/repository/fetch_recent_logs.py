
from google.cloud import logging_v2
from google.protobuf.timestamp_pb2 import Timestamp

def fetch_recent_logs(project_id: str, filter_string: str = None, start_time: str = None, end_time: str = None):
    """
    Retrieves recent log entries from Google Cloud Logging, filtered by field values and time range.

    Args:
        project_id: The Google Cloud project ID.
        filter_string: An advanced logs filter string.
                       (e.g., 'resource.type="cloud_run_revision" AND severity=ERROR')
        start_time: Start of the time range in RFC3339 format (e.g., "2023-01-01T00:00:00Z").
        end_time: End of the time range in RFC3339 format (e.g., "2023-01-01T23:59:59Z").

    Returns:
        A list of log entries.
    """
    client = logging_v2.Client(project=project_id)

    full_filter = []
    if filter_string:
        full_filter.append(filter_string)

    if start_time:
        full_filter.append(f'timestamp>="{start_time}"')
    if end_time:
        full_filter.append(f'timestamp<="{end_time}"')

    filter_str = " AND ".join(full_filter) if full_filter else None

    entries = client.list_entries(
        filter_=filter_str,
        order_by=logging_v2.types.ListLogEntriesRequest.OrderBy.NEWEST
    )

    return list(entries)
