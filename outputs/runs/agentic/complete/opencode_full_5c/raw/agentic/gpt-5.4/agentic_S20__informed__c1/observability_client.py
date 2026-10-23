from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional
import os

from google.cloud import logging_v2

from observability_models import (
    LogQueryWindow,
    StructuredLogEvent,
    normalize_log_entries,
)


def _project_id() -> str:
    value = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not value:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return value


def _default_log_name() -> str:
    return os.environ.get("GCP_LOG_NAME", "application")


def logging_client() -> logging_v2.Client:
    return logging_v2.Client(project=_project_id())


def logger(log_name: Optional[str] = None):
    return logging_client().logger(log_name or _default_log_name())


def write_log_event(
    event: StructuredLogEvent, log_name: Optional[str] = None
) -> Dict[str, Any]:
    entry = event.to_entry()
    payload = dict(entry["jsonPayload"])
    logger(log_name).log_struct(
        payload,
        severity=entry["severity"],
        labels=entry["labels"],
    )
    return entry


def write_log_events(
    events: Iterable[StructuredLogEvent], log_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    return [write_log_event(event, log_name=log_name) for event in events]


def _build_filter(
    window: LogQueryWindow,
    severity: Optional[str] = None,
    field_filters: Optional[Dict[str, str]] = None,
) -> str:
    parts = [
        f'logName="projects/{_project_id()}/logs/{_default_log_name()}"',
        f'timestamp>="{window.start_time}"',
        f'timestamp<="{window.end_time}"',
    ]
    if severity:
        parts.append(f"severity>={severity}")
    for key, value in (field_filters or {}).items():
        parts.append(f'jsonPayload.{key}="{value}"')
    return " AND ".join(parts)


def list_log_entries(
    window: LogQueryWindow,
    severity: Optional[str] = None,
    field_filters: Optional[Dict[str, str]] = None,
    page_size: int = 50,
) -> List[Dict[str, Any]]:
    client = logging_client()
    entries = client.list_entries(
        filter_=_build_filter(window, severity=severity, field_filters=field_filters),
        page_size=page_size,
    )
    items: List[Dict[str, Any]] = []
    for entry in entries:
        payload = (
            entry.payload
            if isinstance(entry.payload, dict)
            else {"message": str(entry.payload)}
        )
        items.append(
            {
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else "",
                "severity": str(entry.severity),
                "labels": dict(entry.labels or {}),
                "jsonPayload": payload,
                "log_name": entry.log_name,
            }
        )
    return items


def query_normalized_logs(
    window: LogQueryWindow,
    severity: Optional[str] = None,
    field_filters: Optional[Dict[str, str]] = None,
    page_size: int = 50,
):
    return normalize_log_entries(
        list_log_entries(
            window, severity=severity, field_filters=field_filters, page_size=page_size
        )
    )
