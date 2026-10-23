import os
from dataclasses import dataclass

from google.cloud import secretmanager


@dataclass
class SecretManagerConfig:
    project_id: str


def load_config() -> SecretManagerConfig:
    project_id = os.environ.get("GCP_PROJECT") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("missing GCP_PROJECT")
    return SecretManagerConfig(project_id=project_id)


def secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_version_path(secret_id: str, version: str = "latest") -> str:
    cfg = load_config()
    return f"projects/{cfg.project_id}/secrets/{secret_id}/versions/{version}"
