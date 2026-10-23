from __future__ import annotations

import os
from datetime import timedelta
from typing import Optional

from google.cloud import monitoring_v3
from google.cloud import storage
from google.oauth2 import service_account

from observability_models import format_rfc3339, utc_now


GOOGLE_CLOUD_MONITORING_SCOPE = "https://www.googleapis.com/auth/monitoring.read"
GOOGLE_CLOUD_STORAGE_SCOPE = "https://www.googleapis.com/auth/devstorage.read_write"


class ObservabilityConfig:
    def __init__(self) -> None:
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.default_bucket = os.getenv("GCS_ARCHIVE_BUCKET")
        self.default_region = os.getenv("GOOGLE_CLOUD_REGION", "global")

    def require_project_id(self) -> str:
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
        return self.project_id


config = ObservabilityConfig()


def _credentials(scopes: Optional[list[str]] = None):
    if config.credentials_path:
        return service_account.Credentials.from_service_account_file(config.credentials_path, scopes=scopes)
    return None


def monitoring_client() -> monitoring_v3.MetricServiceClient:
    creds = _credentials([GOOGLE_CLOUD_MONITORING_SCOPE])
    return monitoring_v3.MetricServiceClient(credentials=creds) if creds else monitoring_v3.MetricServiceClient()


def storage_client() -> storage.Client:
    creds = _credentials([GOOGLE_CLOUD_STORAGE_SCOPE])
    project_id = config.require_project_id()
    return storage.Client(project=project_id, credentials=creds) if creds else storage.Client(project=project_id)


def project_name(project_id: Optional[str] = None) -> str:
    pid = project_id or config.require_project_id()
    return f"projects/{pid}"


def compute_interval(minutes: int) -> tuple[str, str]:
    end = utc_now()
    start = end - timedelta(minutes=minutes)
    return format_rfc3339(start), format_rfc3339(end)
