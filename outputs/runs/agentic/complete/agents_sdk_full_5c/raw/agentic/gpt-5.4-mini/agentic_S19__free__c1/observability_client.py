from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import monitoring_v3


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    location: str = "global"
    metrics_scope: Optional[str] = None


def load_config() -> ObservabilityConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return ObservabilityConfig(
        project_id=project_id,
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
        metrics_scope=os.environ.get("GOOGLE_CLOUD_METRICS_SCOPE"),
    )


def metric_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def project_name(config: Optional[ObservabilityConfig] = None) -> str:
    cfg = config or load_config()
    return f"projects/{cfg.project_id}"


def parse_filters(labels: Optional[Dict[str, str]] = None) -> str:
    labels = labels or {}
    parts = [f'{k} = "{v}"' for k, v in sorted(labels.items())]
    return " AND ".join(parts)
