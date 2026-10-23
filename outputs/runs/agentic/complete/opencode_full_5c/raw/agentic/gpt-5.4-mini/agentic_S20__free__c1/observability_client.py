import os
from typing import Any, Dict

from google.cloud import logging_v2

from observability_models import (
    LogEvent,
    LogQueryRequest,
    normalize_log_event,
    normalize_query_filters,
)


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT", ""))


def get_logging_client() -> logging_v2.Client:
    project_id = get_project_id()
    return logging_v2.Client(project=project_id or None)


def ingest_structured_log(
    event: LogEvent, log_name: str = "application"
) -> Dict[str, Any]:
    client = get_logging_client()
    logger = client.logger(log_name)
    payload = normalize_log_event(event)
    logger.log_struct(payload, severity=event.severity)
    return payload


def query_logs(
    request: LogQueryRequest, log_name: str = "application"
) -> Dict[str, Any]:
    client = get_logging_client()
    filters = normalize_query_filters(request)
    query_parts = [
        f'resource.type="global"',
        f'logName="projects/{client.project}/logs/{log_name}"',
    ]
    if "severity" in filters:
        query_parts.append(f"severity>={filters['severity']}")
    query_parts.append(f'timestamp>="{filters["start_time"]}"')
    query_parts.append(f'timestamp<="{filters["end_time"]}"')
    for key, value in request.field_filters.items():
        query_parts.append(f'jsonPayload.{key}="{value}"')
    entries = list(
        client.list_entries(
            filter_=" AND ".join(query_parts), page_size=filters["limit"]
        )
    )
    return {
        "entries": [dict(e.payload) if hasattr(e, "payload") else {} for e in entries],
        "filters": filters,
    }
