from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import logging_v2
from google.cloud.logging_v2.handlers import CloudLoggingHandler

from observability_models import LogQueryRequest, LogEntryPayload, normalize_labels


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    log_name: str


def load_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
    log_name = os.environ.get("CLOUD_LOG_NAME", "app-log")
    return ObservabilityConfig(project_id=project_id, log_name=log_name)


def get_logging_client(project_id: Optional[str] = None) -> logging_v2.Client:
    return logging_v2.Client(project=project_id or load_config().project_id)


def get_cloud_logging_handler(logger_name: str = "app") -> CloudLoggingHandler:
    client = get_logging_client()
    return CloudLoggingHandler(client, name=logger_name)


def write_structured_entry(payload: LogEntryPayload) -> str:
    cfg = load_config()
    client = get_logging_client(cfg.project_id)
    logger = client.logger(cfg.log_name)
    entry = dict(payload.data)
    if payload.labels:
        entry["labels"] = normalize_labels(payload.labels)
    logger.log_struct(entry, severity=payload.severity)
    return f"projects/{cfg.project_id}/logs/{cfg.log_name}"


def build_filter(request: LogQueryRequest) -> str:
    clauses = []
    if request.severity:
        clauses.append(f'severity>={request.severity}')
    if request.start_time:
        clauses.append(f'timestamp>="{request.start_time.isoformat()}Z"')
    if request.end_time:
        clauses.append(f'timestamp<="{request.end_time.isoformat()}Z"')
    for key, value in (request.fields or {}).items():
        clauses.append(f'jsonPayload.{key}="{value}"')
    return " AND ".join(clauses) if clauses else ""


def query_entries(request: LogQueryRequest):
    cfg = load_config()
    client = get_logging_client(cfg.project_id)
    return list(client.list_entries(filter_=build_filter(request), order_by=logging_v2.DESCENDING, page_size=request.limit))
