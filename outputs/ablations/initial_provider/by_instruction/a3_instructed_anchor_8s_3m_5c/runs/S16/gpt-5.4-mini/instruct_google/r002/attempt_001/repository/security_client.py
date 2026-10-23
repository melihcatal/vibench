import os
from typing import Optional

from google.cloud import secretmanager

from security_models import SecretRef, normalize_secret_text


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT") or ""


def build_secret_name(ref: SecretRef) -> str:
    return f"projects/{ref.project_id}/secrets/{ref.secret_id}/versions/{ref.version}"


def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def access_secret(ref: SecretRef, client: Optional[secretmanager.SecretManagerServiceClient] = None) -> str:
    active_client = client or get_secret_manager_client()
    response = active_client.access_secret_version(request={"name": build_secret_name(ref)})
    return normalize_secret_text(response.payload.data)
