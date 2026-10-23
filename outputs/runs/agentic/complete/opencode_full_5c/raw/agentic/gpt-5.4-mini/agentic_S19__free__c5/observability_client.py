from dataclasses import dataclass
from typing import Any, Dict, Optional
import os

import google.auth
from google.cloud.monitoring_v3 import MetricServiceClient
from google.cloud.storage import Client as StorageClient


@dataclass(frozen=True)
class ObservabilityConfig:
    project_id: str
    location: str
    metric_scope: Optional[str]
    bucket_name: Optional[str]


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        location=os.environ.get("GOOGLE_CLOUD_REGION", "global"),
        metric_scope=os.environ.get("GOOGLE_CLOUD_METRIC_SCOPE"),
        bucket_name=os.environ.get("GOOGLE_CLOUD_STORAGE_BUCKET"),
    )


def monitoring_client() -> MetricServiceClient:
    credentials, _ = google.auth.default()
    return MetricServiceClient(credentials=credentials)


def storage_client() -> StorageClient:
    credentials, _ = google.auth.default()
    return StorageClient(credentials=credentials)


def metric_project_path(project_id: str) -> str:
    return f"projects/{project_id}"


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}
