import os
from typing import Optional

from google.cloud import secretmanager


def get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def build_secret_version_name(secret_id: str, version: Optional[str] = None) -> str:
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    selected_version = version or "latest"
    return f"projects/{project_id}/secrets/{secret_id}/versions/{selected_version}"
