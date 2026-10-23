import os
from dataclasses import dataclass
from typing import Optional
from google.cloud import logging_v2


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    default_log_name: str
    resource_type: str
    api_endpoint: Optional[str] = None


def load_observability_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
    return ObservabilityConfig(
        project_id=project_id,
        default_log_name=os.environ.get("OBSERVABILITY_LOG_NAME", "application"),
        resource_type=os.environ.get("OBSERVABILITY_RESOURCE_TYPE", "global"),
        api_endpoint=os.environ.get("GOOGLE_CLOUD_LOGGING_API_ENDPOINT"),
    )


def build_logging_client(config: Optional[ObservabilityConfig] = None) -> logging_v2.Client:
    cfg = config or load_observability_config()
    return logging_v2.Client(project=cfg.project_id, client_options={"api_endpoint": cfg.api_endpoint} if cfg.api_endpoint else None)


def build_log_name(config: Optional[ObservabilityConfig] = None, suffix: Optional[str] = None) -> str:
    cfg = config or load_observability_config()
    name = cfg.default_log_name
    if suffix:
        name = f"{name}/{suffix}"
    return name
