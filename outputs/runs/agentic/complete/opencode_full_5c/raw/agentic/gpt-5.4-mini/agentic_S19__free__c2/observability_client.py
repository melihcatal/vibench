import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import monitoring_v3


@dataclass
class ObservabilityConfig:
    project_id: str
    metric_prefix: str = ""
    location: str = "global"


def load_config() -> ObservabilityConfig:
    project_id = (
        os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
    )
    metric_prefix = os.environ.get("METRIC_PREFIX", "")
    location = os.environ.get("METRIC_LOCATION", "global")
    return ObservabilityConfig(
        project_id=project_id, metric_prefix=metric_prefix, location=location
    )


def monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def project_name(config: Optional[ObservabilityConfig] = None) -> str:
    cfg = config or load_config()
    return f"projects/{cfg.project_id}"


def normalize_metric_name(
    name: str, config: Optional[ObservabilityConfig] = None
) -> str:
    cfg = config or load_config()
    return f"{cfg.metric_prefix}{name}"


def to_time_interval(start: Any, end: Any) -> Dict[str, Any]:
    return {"start_time": start, "end_time": end}
