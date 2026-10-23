import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from google.cloud import logging_v2


@dataclass
class ObservabilityConfig:
    project_id: str
    log_name: str
    default_severity: str = "INFO"


def load_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    log_name = os.environ.get("GOOGLE_CLOUD_LOG_NAME", "application-log")
    return ObservabilityConfig(project_id=project_id, log_name=log_name)


def client_for_project(project_id: Optional[str] = None) -> logging_v2.Client:
    cfg = load_config()
    return logging_v2.Client(project=project_id or cfg.project_id)


def timestamp_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_labels(labels: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    normalized: Dict[str, str] = {}
    for key, value in (labels or {}).items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


def severity_from_text(value: Optional[str]) -> str:
    if not value:
        return "INFO"
    return value.upper()
