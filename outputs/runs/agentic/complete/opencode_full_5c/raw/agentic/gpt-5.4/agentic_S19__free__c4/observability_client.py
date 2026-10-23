from __future__ import annotations

import os
from typing import Dict

from google.cloud import monitoring_v3
from google.cloud import storage
from google.oauth2 import service_account


def load_google_credentials():
    credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credential_path:
        return service_account.Credentials.from_service_account_file(credential_path)
    return None


def monitoring_client() -> monitoring_v3.MetricServiceClient:
    credentials = load_google_credentials()
    if credentials is not None:
        return monitoring_v3.MetricServiceClient(credentials=credentials)
    return monitoring_v3.MetricServiceClient()


def storage_client() -> storage.Client:
    credentials = load_google_credentials()
    project = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if credentials is not None:
        return storage.Client(project=project, credentials=credentials)
    return storage.Client(project=project)


def project_resource_name(project_id: str) -> str:
    return f"projects/{project_id}"


def build_monitoring_filter(
    metric_type: str, labels: Dict[str, str] | None = None
) -> str:
    parts = [f'metric.type = "{metric_type}"']
    for key, value in (labels or {}).items():
        if (
            key.startswith("resource.labels.")
            or key.startswith("metric.labels.")
            or key.startswith("resource.type")
        ):
            parts.append(f'{key} = "{value}"')
        else:
            parts.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(parts)
