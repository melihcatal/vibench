import os
import datetime
from google.cloud import logging
from observability_client import get_logging_client
from observability_models import LogEntry

def query_error_logs(log_name: str, time_ago_minutes: int = 60) -> list[LogEntry]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = get_logging_client()

    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(minutes=time_ago_minutes)

    # Filter for ERROR or higher severity and specific log name
    # Note: Google Cloud Logging uses 'severity' for levels like ERROR, WARNING, INFO
    # The full filter syntax is documented at: https://cloud.google.com/logging/docs/view/logging-query-language
    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'severity>=ERROR '
        f'timestamp>="{start_time.isoformat(timespec="seconds")}" '
        f'timestamp<="{end_time.isoformat(timespec="seconds")}"'
    )

    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    results = []
    for entry in entries:
        # Convert Google Cloud Logging Entry to our internal LogEntry model
        results.append(LogEntry(
            log_name=entry.log_name.split('/')[-1] if entry.log_name else '',
            timestamp=entry.timestamp.isoformat() if entry.timestamp else '',
            severity=entry.severity or 'UNKNOWN',
            message=entry.payload.get('message') if isinstance(entry.payload, dict) else str(entry.payload),
            json_payload=entry.json_payload or {}
        ))
    return results

