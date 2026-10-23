import os
from datetime import datetime, timedelta
from google.cloud import logging_v2

from observability_client import get_logging_v2_client
from observability_models import LogSeverity, QueryResult

def query_error_logs(project_id: str, minutes_ago: int = 60) -> list[QueryResult]:
    client = get_logging_v2_client()

    now = datetime.utcnow()
    time_filter = (now - timedelta(minutes=minutes_ago)).isoformat(
        timespec='milliseconds'
    ) + 'Z'

    # Google Cloud Logging's advanced filter syntax
    # Filters for severity 'ERROR' or 'CRITICAL' and recent logs
    filter_string = f"severity=(\"ERROR\" OR \"CRITICAL\") AND timestamp >= \"{time_filter}\""

    entries = client.list_log_entries(
        project_ids=[project_id],
        filter_=filter_string,
        order_by="timestamp desc"
    )

    results = []
    for entry in entries:
        message = entry.json_payload.get('message') if entry.json_payload else entry.text_payload
        severity = entry.severity.name if entry.severity else LogSeverity.UNKNOWN.value
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

