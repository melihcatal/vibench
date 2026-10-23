from datetime import datetime, timedelta, timezone
from google.cloud import logging_v2

from observability_client import get_logging_client
from observability_models import LogEntry, QueryLogRequest, QueryLogResponse


def fetch_recent_logs(request: QueryLogRequest) -> QueryLogResponse:
    client = get_logging_client(request.project_id)

    entries = []
    for entry in client.list_entries(
        project_ids=[request.project_id],
        filter_=request.filter_expression,
        order_by=request.order_by,
        page_size=request.page_size,
        page_token=request.page_token,
    ):
        resource_labels = dict(entry.resource.labels) if entry.resource else {}
        entries.append(
            LogEntry(
                timestamp=entry.timestamp,
                severity=entry.severity.name,
                message=entry.text_payload if entry.text_payload else str(entry.json_payload),
                resource_type=entry.resource.type if entry.resource else "unknown",
                resource_labels=resource_labels,
                json_payload=entry.json_payload if entry.json_payload else None,
                text_payload=entry.text_payload if entry.text_payload else None,
                trace=entry.trace,
                span_id=entry.span_id,
                insert_id=entry.insert_id,
            )
        )

    next_page_token = None  # Placeholder

    return QueryLogResponse(entries=entries, next_page_token=next_page_token)
