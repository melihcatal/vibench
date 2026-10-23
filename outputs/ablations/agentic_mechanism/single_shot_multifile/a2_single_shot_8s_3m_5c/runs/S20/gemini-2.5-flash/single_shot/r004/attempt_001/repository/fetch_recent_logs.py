import os
import datetime
from google.cloud import logging
from observability_client import get_logging_client
from observability_models import LogEntry

def fetch_recent_logs(log_name: str, time_ago_minutes: int = 30, filters: dict = None) -> list[LogEntry]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_logging_client()

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(minutes=time_ago_minutes)

    base_filter = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}" '
        f'timestamp<="{end_time.isoformat(timespec="seconds")}"'
    )

    if filters:
        for field, value in filters.items():
            # For JSON payload fields, use jsonPayload.field_name or equivalent
            if field.startswith('jsonPayload.'):
                base_filter += f' {field}="{value}"'
            else:
                # For top-level fields like severity, textPayload, etc.
                base_filter += f' {field}="{value}"'

    entries = client.list_entries(filter_=base_filter, order_by=logging.DESCENDING)

    results = []
    for entry in entries:
        results.append(LogEntry(
            log_name=entry.log_name.split('/')[-1] if entry.log_name else '',
            timestamp=entry.timestamp.isoformat() if entry.timestamp else '',
            severity=entry.severity or 'UNKNOWN',
            message=entry.payload.get('message') if isinstance(entry.payload, dict) else str(entry.payload),
            json_payload=entry.json_payload or {}
        ))
    return results

