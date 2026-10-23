"""Local configuration and client helper utilities for Managed Log Query / Log Ingestion."""

import os
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Iterator, List, Optional

from google.cloud import logging as google_logging
from google.cloud.logging_v2 import Client as LoggingClient
from google.cloud.logging_v2.entries import LogEntry as GCLogEntry

from observability_models import (
    LogEntry,
    LogEvent,
    LogQueryRequest,
    LogQueryResponse,
)


def get_google_cloud_logging_client(project_id: Optional[str] = None) -> LoggingClient:
    """Create and return a Google Cloud Logging client using GOOGLE_APPLICATION_CREDENTIALS."""
    return LoggingClient(project=project_id)


def build_log_resource_name(project_id: str, log_id: str) -> str:
    """Build a Google Cloud Logging log resource name."""
    return f"projects/{project_id}/logs/{log_id}"


def format_time_range_filter(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> str:
    """Build a Google Cloud Logging time range filter string."""
    parts = []
    if start_time:
        ts = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        parts.append(f'timestamp>="{ts}"')
    if end_time:
        ts = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        parts.append(f'timestamp<="{ts}"')
    return " AND ".join(parts) if parts else ""


def build_severity_filter(severity: str) -> str:
    """Build a severity filter string for Google Cloud Logging."""
    return f'severity="{severity.upper()}"'


def build_label_filter(labels: Dict[str, str]) -> str:
    """Build label-based filter expressions for Google Cloud Logging."""
    parts = []
    for key, value in labels.items():
        parts.append(f'labels.{key}="{value}"')
    return " AND ".join(parts)


def normalize_gcloud_entries(
    entries: List[GCLogEntry],
) -> List[LogEntry]:
    """Normalize Google Cloud Logging entries into local LogEntry objects."""
    normalized = []
    for entry in entries:
        payload = entry.payload
        message = ""
        if isinstance(payload, str):
            message = payload
        elif isinstance(payload, dict):
            message = payload.get("message", str(payload))
        elif payload is not None:
            message = str(payload)

        labels = {}
        if hasattr(entry, "labels") and entry.labels:
            labels = dict(entry.labels)

        normalized.append(LogEntry(
            timestamp=entry.timestamp or datetime.now(timezone.utc),
            severity=entry.severity or "DEFAULT",
            message=message,
            resource_type=entry.resource.type if hasattr(entry, "resource") and entry.resource else "",
            labels=labels,
            trace_id=entry.trace,
            correlation_id=labels.get("correlation_id"),
        ))
    return normalized


@contextmanager
def get_logging_client_context(
    project_id: Optional[str] = None,
) -> Iterator[LoggingClient]:
    """Context manager providing a Google Cloud Logging client."""
    client = get_google_cloud_logging_client(project_id=project_id)
    try:
        yield client
    finally:
        pass
