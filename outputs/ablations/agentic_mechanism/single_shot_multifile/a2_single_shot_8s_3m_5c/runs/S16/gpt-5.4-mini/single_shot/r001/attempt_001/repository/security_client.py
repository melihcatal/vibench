import os
from functools import lru_cache
from typing import Optional
from google.cloud import secretmanager


@lru_cache(maxsize=1)
def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or os.environ.get("GCLOUD_PROJECT") or ""


def resolve_secret_name(secret_name: str) -> str:
    if secret_name.startswith("projects/"):
        return secret_name
    project_id = get_project_id()
    if not project_id:
        raise ValueError("Missing Google Cloud project id")
    return f"projects/{project_id}/secrets/{secret_name}"


def secret_version_path(secret_resource: str, version: str) -> str:
    return f"{secret_resource}/versions/{version}"
