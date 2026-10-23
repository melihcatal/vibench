import os
from dataclasses import dataclass

from google.cloud import monitoring_v3


@dataclass
class ObservabilityConfig:
    project_id: str
    period_seconds: int = 60


def load_config(config=None):
    config = config or {}
    project_id = config.get("project_id") or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    if not project_id:
        raise ValueError("project_id is required")
    return ObservabilityConfig(project_id=project_id, period_seconds=int(config.get("period_seconds", 60)))


def metric_client():
    return monitoring_v3.MetricServiceClient()


def project_name(config):
    cfg = config if isinstance(config, ObservabilityConfig) else load_config(config)
    return f"projects/{cfg.project_id}"
