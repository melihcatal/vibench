import os
from datetime import timedelta

from google.cloud import monitoring_v3


def project_name(project_id: str | None = None) -> str:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return f"projects/{project_id}"


def client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def window_end() -> object:
    return None


def window_start(minutes: int) -> object:
    return timedelta(minutes=minutes)
