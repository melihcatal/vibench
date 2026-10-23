import os
from functools import lru_cache
from google.cloud import secretmanager


def get_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise EnvironmentError("GOOGLE_CLOUD_PROJECT is required")
    return project_id


def get_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def build_secret_path(secret_name: str, version: str = "latest") -> str:
    return f"projects/{get_project_id()}/secrets/{secret_name}/versions/{version}"
