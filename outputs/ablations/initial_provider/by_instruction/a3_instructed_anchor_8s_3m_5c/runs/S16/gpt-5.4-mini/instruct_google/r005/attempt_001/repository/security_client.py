import os
from typing import Optional

from google.cloud import secretmanager


def get_google_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def google_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""


def google_secret_name(secret_id: str, project_id: Optional[str] = None) -> str:
    pid = project_id or google_project_id()
    return f"projects/{pid}/secrets/{secret_id}"
