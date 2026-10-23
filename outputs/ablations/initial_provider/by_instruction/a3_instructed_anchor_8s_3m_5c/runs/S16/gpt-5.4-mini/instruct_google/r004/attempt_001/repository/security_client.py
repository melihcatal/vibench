import os
from dataclasses import dataclass

from google.cloud import secretmanager


@dataclass
class SecretClientConfig:
    project_id: str
    secret_id: str
    version_id: str = "latest"


def load_config(secret_id: str, version_id: str = "latest") -> SecretClientConfig:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return SecretClientConfig(project_id=project_id, secret_id=secret_id, version_id=version_id)


def build_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_version_path(config: SecretClientConfig) -> str:
    return f"projects/{config.project_id}/secrets/{config.secret_id}/versions/{config.version_id}"


def secret_payload_text(response) -> str:
    return response.payload.data.decode("utf-8")
