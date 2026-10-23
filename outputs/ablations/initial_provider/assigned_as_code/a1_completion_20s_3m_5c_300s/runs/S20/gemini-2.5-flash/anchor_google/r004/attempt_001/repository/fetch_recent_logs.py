from datetime import datetime, timedelta
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import QueryLogRequest, LogEntry

def fetch_recent_logs(
    project_id: str,
    minutes_ago: int = 60,
    log_name: str = None,
    field_filters: Dict[str, Any] = None,
    limit: int = 100
):
    client = ObservabilityClient(project_id=project_id)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes_ago)

    filter_parts = [
        f"timestamp >= \"{start_time.isoformat()}\"",
        f"timestamp < \"{end_time.isoformat()}\""
    ]
    if log_name:
        filter_parts.append(f"logName=\"projects/{project_id}/logs/{log_name}\"")

    if field_filters:
        for field, value in field_filters.items():
            if isinstance(value, str):
                filter_parts.append(f"{field}=\"{value}\"")
            else:
                filter_parts.append(f"{field}={value}")

    filter_expression = " AND ".join(filter_parts)

    query_request = QueryLogRequest(
        project_id=project_id,
        filter_expression=filter_expression,
        order_by="timestamp desc",
        limit=limit
    )

    entries_iterator = client.get_logging_entries(
        filter_expression=query_request.filter_expression,
        order_by=query_request.order_by,
        page_size=query_request.limit
    )

    recent_logs = []
    for entry in entries_iterator:
        payload = entry.json_payload or entry.text_payload or str(entry.proto_payload)
        recent_logs.append(LogEntry(
            timestamp=entry.timestamp.replace(tzinfo=None) if entry.timestamp else datetime.utcnow(),
            severity=entry.severity,
            message=str(payload),
            labels=dict(entry.labels) if entry.labels else {},
            trace_id=entry.trace,
            span_id=entry.span_id
        ))

    return {"recent_log_count": len(recent_logs), "recent_logs": [log.model_dump(by_alias=True, exclude_none=True) for log in recent_logs]}
