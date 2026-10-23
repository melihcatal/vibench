from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client
from observability_models import LogEntry, LogQueryResponse
import os

def fetch_recent_logs(log_name: str, field_filters: dict = None, time_range_seconds: int = 3600, page_size: int = 100) -> LogQueryResponse:
    client = get_logging_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    now = datetime.now(timezone.utc)
    start_time = (now - timedelta(seconds=time_range_seconds)).isoformat(timespec='seconds') + 'Z'
    end_time = now.isoformat(timespec='seconds') + 'Z'

    filter_parts = [
        f'resource.type="global"',
        f'logName="projects/{project_id}/logs/{log_name}"',
        f'timestamp>="{start_time}"',
        f'timestamp<="{end_time}"',
    ]

    if field_filters:
        for field, value in field_filters.items():
            # This handles nested JSON fields as well, e.g., jsonPayload.request.method
            filter_parts.append(f'{field}="{value}"')

    filter_string = " AND ".join(filter_parts)

    entries_iterator = client.list_entries(
        project_ids=[project_id],
        filter_=filter_string,
        order_by=logging_v2.entries.ListLogEntriesRequest.OrderBy.NEWEST,
        page_size=page_size
    )

    log_entries = []
    for entry in entries_iterator:
        message = entry.text_payload if entry.text_payload else str(entry.json_payload) if entry.json_payload else entry.proto_payload
        severity = entry.severity.name
        timestamp = entry.timestamp.replace(tzinfo=timezone.utc)
        labels = dict(entry.labels)
        json_payload = dict(entry.json_payload) if entry.json_payload else None

        log_entries.append(LogEntry(message, severity, timestamp, labels, json_payload))

    return LogQueryResponse(entries=log_entries)
