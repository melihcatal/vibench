import os
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

from google.cloud import logging as cloud_logging
from google.cloud import bigquery


@dataclass
class ObservabilityConfig:
    project_id: str
    log_name: str
    dataset_id: str
    table_id: str


def load_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
    log_name = os.environ.get("GOOGLE_CLOUD_LOG_NAME", "applications")
    dataset_id = os.environ.get("BIGQUERY_DATASET_ID", "observability")
    table_id = os.environ.get("BIGQUERY_TABLE_ID", "log_events")
    return ObservabilityConfig(project_id=project_id, log_name=log_name, dataset_id=dataset_id, table_id=table_id)


def build_logging_client(project_id: Optional[str] = None) -> cloud_logging.Client:
    cfg = load_config()
    return cloud_logging.Client(project=project_id or cfg.project_id or None)


def build_bigquery_client(project_id: Optional[str] = None) -> bigquery.Client:
    cfg = load_config()
    return bigquery.Client(project=project_id or cfg.project_id or None)


def time_window(minutes: int = 30) -> tuple[datetime, datetime]:
    end = datetime.now(timezone.utc)
    return end - timedelta(minutes=minutes), end


def isoformat(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, datetime):
            normalized[key] = isoformat(value)
        else:
            normalized[key] = value
    return normalized
