import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import logging_v2
from google.cloud.logging_v2.handlers.transports.background_thread import BackgroundThreadTransport

from observability_models import normalize_log_fields, normalize_severity


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    log_name: str
    default_resource_type: str


@lru_cache(maxsize=1)
def get_config() -> ObservabilityConfig:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("Missing Google Cloud project id. Set GOOGLE_CLOUD_PROJECT, GCP_PROJECT, or GOOGLE_PROJECT_ID.")
    return ObservabilityConfig(
        project_id=project_id,
        log_name=os.getenv("OBSERVABILITY_LOG_NAME", "application"),
        default_resource_type=os.getenv("OBSERVABILITY_RESOURCE_TYPE", "global"),
    )


@lru_cache(maxsize=1)
def get_logging_client() -> logging_v2.Client:
    return logging_v2.Client(project=get_config().project_id)


def get_logger(log_name: Optional[str] = None) -> logging_v2.Logger:
    return get_logging_client().logger(log_name or get_config().log_name)


def write_structured_entry(payload: Dict[str, Any], severity: str = "INFO", log_name: Optional[str] = None) -> str:
    logger = get_logger(log_name)
    normalized = normalize_log_fields(payload)
    severity_name = normalize_severity(severity)
    logger.log_struct(normalized, severity=severity_name, resource={"type": get_config().default_resource_type, "labels": {}})
    return normalized.get("insert_id", "")


def write_text_entry(text: str, severity: str = "INFO", labels: Optional[Dict[str, str]] = None, log_name: Optional[str] = None) -> None:
    logger = get_logger(log_name)
    logger.log_text(
        text,
        severity=normalize_severity(severity),
        labels=labels or {},
        resource={"type": get_config().default_resource_type, "labels": {}},
        transport=BackgroundThreadTransport,
    )


def query_log_entries(filter_: str, page_size: int = 100):
    client = get_logging_client()
    return client.list_entries(filter_=filter_, page_size=page_size)
