from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from observability_models import LogEntry, LogQueryResponse
import os

def query_error_logs(log_name: str, min_severity: str = "ERROR", time_range_seconds: int = 3600, page_size: int = 100) -> LogQueryResponse:
    client = get_logging_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    now = datetime.now(timezone.utc)
    # Google Cloud Logging filter expects RFC3339 format
    start_time = (now - timedelta(seconds=time_range_seconds)).isoformat(timespec='seconds') + 'Z'
    end_time = now.isoformat(timespec='seconds') + 'Z'

    # Construct the filter string. Note the specific syntax for resource.type and timestamp range.
    filter_string = (
        f'resource.type="global" AND '  # Assuming global resource type as in write_structured_log.py
        f'logName="projects/{project_id}/logs/{log_name}" AND '
        f'severity>="{min_severity}" AND '
        f'timestamp>="{start_time}" AND '
        f'timestamp<="{end_time}"'
    )

    # Use client.list_entries with the constructed filter
    entries_iterator = client.list_entries(
        project_ids=[project_id],
        filter_=filter_string,
        order_by=logging_v2.entries.ListLogEntriesRequest.OrderBy.NEWEST,
        page_size=page_size
    )

    log_entries = []
    for entry in entries_iterator:
        # Extract relevant fields from the LogEntry object
        message = entry.text_payload if entry.text_payload else str(entry.json_payload) if entry.json_payload else entry.proto_payload
        severity = entry.severity.name
        timestamp = entry.timestamp.replace(tzinfo=timezone.utc)
        labels = dict(entry.labels)
        json_payload = dict(entry.json_payload) if entry.json_payload else None

        log_entries.append(LogEntry(message, severity, timestamp, labels, json_payload))

    # Note: Google Cloud Logging client automatically handles pagination through the iterator.
    # We don't directly get a next_page_token in this simple iteration. For explicit pagination,
    # more advanced handling of the iterator would be needed.
    return LogQueryResponse(entries=log_entries)
