from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import monitoring_v3, storage


@dataclass(frozen=True)
class ManagedMetricsConfig:
    project_id: str
    metrics_scope: Optional[str] = None
    storage_bucket: Optional[str] = None
    translate_location: str = "global"


def load_config() -> ManagedMetricsConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return ManagedMetricsConfig(
        project_id=project_id,
        metrics_scope=os.environ.get("METRICS_SCOPE"),
        storage_bucket=os.environ.get("METRICS_EXPORT_BUCKET"),
        translate_location=os.environ.get("CLOUD_TRANSLATE_LOCATION", "global"),
    )


def monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def storage_client() -> storage.Client:
    return storage.Client()


def project_name(project_id: str) -> str:
    return f"projects/{project_id}"
