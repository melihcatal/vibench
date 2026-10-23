from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQueryResult
from datetime import datetime, timedelta, timezone
import os

def fetch_recent_logs(project_id: str = None, hours_ago: int = 1, filter_fields: dict = None):
    client = ObservabilityClient(project_id=project_id)
    
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_ago)

    filter_parts = [f'timestamp>=\"{start_time.isoformat()}\" AND timestamp<="{end_time.isoformat()}"'
    ]

    if filter_fields:
        for key, value in filter_fields.items():
            # Basic escaping for string values to avoid injection issues, assuming simple key-value filters
            escaped_value = str(value).replace("'", "\'").replace("\"", "\\\"")
            filter_parts.append(f'{key}=\"{escaped_value}\'')
    
    filter_string = " AND ".join(filter_parts)
    
    entries_iterator = client.list_log_entries(filter_string=filter_string, order_by="timestamp desc")
    
    results = []
    for entry in entries_iterator:
        log_entry_model = LogEntry(
            severity=entry.severity,
            message=entry.payload.get("message", str(entry.payload)) if isinstance(entry.payload, dict) else str(entry.payload),
            resource_type=entry.resource.type if entry.resource else "unknown",
            resource_id=entry.resource.labels.get("resource_id", "") if entry.resource and entry.resource.labels else "",
            timestamp=entry.timestamp.isoformat(),
            labels=dict(entry.labels) if entry.labels else None,
            json_payload=entry.json_payload if entry.json_payload else None,
            text_payload=entry.text_payload if entry.text_payload else None,
            trace=entry.trace,
            span_id=entry.span_id,
            trace_sampled=entry.trace_sampled
        )
        results.append(log_entry_model)

    return LogQueryResult(entries=results)
