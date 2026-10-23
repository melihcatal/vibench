from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import QueryLogRequest, LogEntry

def query_error_logs(project_id: str, minutes_ago: int = 60, log_name: str = None):
    client = ObservabilityClient(project_id=project_id)
    
    # Calculate the timestamp for the filter
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes_ago)

    filter_parts = [
        "severity >= ERROR",
        f"timestamp >= \"{start_time.isoformat()}\"",
        f"timestamp < \"{end_time.isoformat()}\""
    ]
    if log_name:
        filter_parts.append(f"logName=\"projects/{project_id}/logs/{log_name}\"")

    filter_expression = " AND ".join(filter_parts)

    query_request = QueryLogRequest(
        project_id=project_id,
        filter_expression=filter_expression,
        order_by="timestamp desc",
        limit=100 # Adjust as needed
    )

    entries_iterator = client.get_logging_entries(
        filter_expression=query_request.filter_expression,
        order_by=query_request.order_by,
        page_size=query_request.limit
    )

    error_logs = []
    for entry in entries_iterator:
        # Google Cloud Logging returns Entry objects, convert to our LogEntry model if needed
        # For simplicity, we'll just extract relevant fields for now
        payload = entry.json_payload or entry.text_payload or str(entry.proto_payload)
        error_logs.append(LogEntry(
            timestamp=entry.timestamp.replace(tzinfo=None) if entry.timestamp else datetime.utcnow(),
            severity=entry.severity,
            message=str(payload),
            labels=dict(entry.labels) if entry.labels else {},
            trace_id=entry.trace,
            span_id=entry.span_id
        ))
    
    return {"error_log_count": len(error_logs), "error_logs": [log.model_dump(by_alias=True, exclude_none=True) for log in error_logs]}
