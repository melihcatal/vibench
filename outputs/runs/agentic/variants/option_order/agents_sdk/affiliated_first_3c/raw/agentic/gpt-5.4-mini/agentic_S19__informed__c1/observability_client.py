from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import monitoring_v3


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    credentials_path: Optional[str] = None

    @classmethod
    def from_env(cls) -> "ObservabilityConfig":
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or os.environ.get("PROJECT_ID")
        if not project_id:
            raise ValueError("Missing Google Cloud project identifier in GOOGLE_CLOUD_PROJECT, GCP_PROJECT, or PROJECT_ID")
        return cls(project_id=project_id, credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))


def create_metric_client(config: Optional[ObservabilityConfig] = None) -> monitoring_v3.MetricServiceClient:
    config = config or ObservabilityConfig.from_env()
    return monitoring_v3.MetricServiceClient()


def project_name(config: Optional[ObservabilityConfig] = None) -> str:
    config = config or ObservabilityConfig.from_env()
    return f"projects/{config.project_id}"
