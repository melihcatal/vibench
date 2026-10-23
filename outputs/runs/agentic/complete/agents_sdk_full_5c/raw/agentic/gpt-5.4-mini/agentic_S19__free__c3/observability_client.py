from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import monitoring_v3
from google.cloud import storage


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    metric_scope_project: Optional[str] = None
    storage_bucket: Optional[str] = None


@lru_cache(maxsize=1)
def load_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
    return ObservabilityConfig(
        project_id=project_id,
        metric_scope_project=os.environ.get("METRIC_SCOPE_PROJECT"),
        storage_bucket=os.environ.get("METRICS_ARCHIVE_BUCKET"),
    )


@lru_cache(maxsize=1)
def monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


@lru_cache(maxsize=1)
def storage_client() -> storage.Client:
    return storage.Client()


def monitored_project_name(project_id: Optional[str] = None) -> str:
    cfg = load_config()
    return f"projects/{project_id or cfg.metric_scope_project or cfg.project_id}"


def extract_label_map(metric: Any) -> Dict[str, str]:
    labels: Dict[str, str] = {}
    for k, v in getattr(metric, "resource", {}).items() if isinstance(getattr(metric, "resource", {}), dict) else []:
        labels[str(k)] = str(v)
    return labels
