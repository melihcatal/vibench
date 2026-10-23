import os
from datetime import datetime, timedelta
from google.cloud import logging_v2

from observability_client import get_logging_v2_client
from observability_models import QueryResult

def fetch_recent_logs(project_id: str, log_name_prefix: str, field_filters: dict = None, minutes_ago: int = 30) -> list[QueryResult]:
    client = get_logging_v2_client()

    now = datetime.utcnow()
    time_filter = (now - timedelta(minutes=minutes_ago)).isoformat(
        timespec='milliseconds'
    ) + 'Z'

    # Google Cloud Logging's advanced filter syntax
    filter_parts = [
        f"logName:(\"{log_name_prefix}\")", # Assuming log_name_prefix is like projects/<PROJECT_ID>/logs/app-log
        f"timestamp >= \"{time_filter}\""
    ]

    if field_filters:
        for field, value in field_filters.items():
            # For JSON payloads, field values are accessed via jsonPayload.field_name
            filter_parts.append(f"jsonPayload.{field}=\"{value}\"")

    filter_string = " AND ".join(filter_parts)

    entries = client.list_log_entries(
        project_ids=[project_id],
        filter_=filter_string,
        order_by="timestamp desc"
    )

    results = []
    for entry in entries:
        message = entry.json_payload.get('message') if entry.json_payload else entry.text_payload
        severity = entry.severity.name if entry.severity else "UNKNOWN"
        timestamp = entry.timestamp.isoformat()
        resource_type = entry.resource.type if entry.resource else ""

        results.append(
            QueryResult(
                log_id=entry.log_name,
                timestamp=timestamp,
                severity=severity,
                message=message if message else "[No message]",
                resource_type=resource_type,
                full_entry=entry.json_payload if entry.json_payload else {"text_payload": entry.text_payload}
            )
        )
    return results

