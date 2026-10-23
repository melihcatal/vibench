from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Iterable

from google.cloud import logging_v2

from observability_models import StructuredLogEvent, ensure_rfc3339


DEFAULT_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
DEFAULT_LOG_NAME_ENV = "GCP_LOG_NAME"
DEFAULT_RESOURCE_TYPE_ENV = "GCP_LOG_RESOURCE_TYPE"
DEFAULT_RESOURCE_LABELS_PREFIX = "GCP_RESOURCE_LABEL_"


def get_project_id() -> str:
    project_id = os.getenv(DEFAULT_PROJECT_ENV)
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required for Google Cloud Logging")
    return project_id


def get_log_name() -> str:
    return os.getenv(DEFAULT_LOG_NAME_ENV, "application")


def get_resource() -> dict[str, object]:
    labels = {
        key[len(DEFAULT_RESOURCE_LABELS_PREFIX):].lower(): value
        for key, value in os.environ.items()
        if key.startswith(DEFAULT_RESOURCE_LABELS_PREFIX)
    }
    return {
        "type": os.getenv(DEFAULT_RESOURCE_TYPE_ENV, "global"),
        "labels": labels,
    }


def get_logging_client() -> logging_v2.Client:
    return logging_v2.Client(project=get_project_id())


def get_logger() -> logging_v2.logger.Logger:
    return get_logging_client().logger(get_log_name())


def write_structured_event(event: StructuredLogEvent) -> None:
    logger = get_logger()
    logger.log_struct(
        info=event.to_cloud_logging_entry(),
        severity=event.severity,
        resource=get_resource(),
    )


def build_time_range_filter(start_time: datetime, end_time: datetime) -> str:
    return f'timestamp >= "{ensure_rfc3339(start_time)}" AND timestamp <= "{ensure_rfc3339(end_time)}"'


def recent_window(minutes: int = 15) -> tuple[datetime, datetime]:
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    return start_time, end_time


def join_filter_parts(parts: Iterable[str]) -> str:
    return " AND ".join(part for part in parts if part)
