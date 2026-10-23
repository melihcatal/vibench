import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from google.cloud import logging as google_cloud_logging
from google.cloud.logging_v2.entries import LogEntry
from google.cloud.logging_v2.client import Client

from observability_models import LogEvent, LogQuery, isoformat_utc, records_from_response


def _project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def create_client(project_id: Optional[str] = None) -> Client:
    return google_cloud_logging.Client(project=project_id or _project_id())


def write_event(event: LogEvent, log_name: str = "app-log", project_id: Optional[str] = None) -> Dict[str, Any]:
    client = create_client(project_id)
    logger = client.logger(log_name)
    payload = event.to_dict()
    logger.log_struct(payload, severity=event.severity)
    return payload


def query_entries(query: LogQuery, log_name: Optional[str] = None, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
    client = create_client(project_id)
    filters = []
    if log_name:
        filters.append(f'logName="projects/{client.project}/logs/{log_name}"')
    if query.severity:
        filters.append(f'severity>={query.severity}')
    if query.start_time:
        filters.append(f'timestamp>="{query.start_time}"')
    if query.end_time:
        filters.append(f'timestamp<="{query.end_time}"')
    for key, value in (query.field_filters or {}).items():
        filters.append(f'jsonPayload.{key}="{value}"')
    filter_text = " AND ".join(filters) if filters else None
    entries = client.list_entries(filter_=filter_text, page_size=query.limit)
    response: List[Dict[str, Any]] = []
    for entry in entries:
        payload = getattr(entry, "payload", {})
        response.append({
            "timestamp": getattr(entry, "timestamp", None).isoformat() if getattr(entry, "timestamp", None) else None,
            "severity": getattr(entry, "severity", None),
            "payload": payload,
            "log_name": getattr(entry, "log_name", None),
        })
    return records_from_response(response)


def recent_time_window(minutes: int = 15) -> Dict[str, str]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return {"start_time": isoformat_utc(start), "end_time": isoformat_utc(end)}
