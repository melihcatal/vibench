from observability_client import clients
from observability_models import LogQueryResult
from datetime import datetime, timedelta
from typing import List, Optional

def query_error_logs(
    project_id: str,
    log_name: Optional[str] = None,
    time_range_seconds: int = 3600,
    min_severity: str = "ERROR",
    limit: int = 100
) -> List[LogQueryResult]:
    """
    Queries recent error log entries from Google Cloud Logging, filtered by severity and time range.
    """
    gcp_logging_client = clients.gcp_logging_client

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(seconds=time_range_seconds)

    filters = [
        f'severity >= {min_severity}',
        f'timestamp >= "{start_time.isoformat("T")+"Z"}"',
        f'timestamp < "{end_time.isoformat("T")+"Z"}"'
    ]
    if log_name:
        filters.append(f'logName="projects/{project_id}/logs/{log_name}"')
    
    filter_string = " AND ".join(filters)

    entries_iterator = gcp_logging_client.list_entries(
        project_ids=[project_id],
        filter_=filter_string,
        order_by="timestamp desc",
        page_size=limit
    )

    results: List[LogQueryResult] = []
    for entry in entries_iterator:
        payload = {}
        if entry.json_payload:
            payload = entry.json_payload
            message = payload.get("message", str(payload))
        elif entry.text_payload:
            message = entry.text_payload
        else:
            message = str(entry.proto_payload) if entry.proto_payload else "No payload"

        results.append(
            LogQueryResult(
                timestamp=entry.timestamp.replace(tzinfo=None),
                severity=entry.severity,
                message=message,
                payload=payload,
                log_name=entry.log_name.split('/')[-1],
                resource={
                    "type": entry.resource.type,
                    "labels": dict(entry.resource.labels)
                },
                trace_id=entry.trace,
                span_id=entry.span_id
            )
        )
        if len(results) >= limit:
            break
    
    return results
