import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import secretmanager


@dataclass(frozen=True)
class SecretManagerConfig:
    project_id: str
    secret_id: str
    version_id: str = "latest"


def load_config(prefix: str = "SECRET_") -> SecretManagerConfig:
    project_id = os.getenv(f"{prefix}PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    secret_id = os.getenv(f"{prefix}ID") or os.getenv("SECRET_ID")
    version_id = os.getenv(f"{prefix}VERSION", "latest")
    if not project_id:
        raise ValueError("Missing secret manager project id")
    if not secret_id:
        raise ValueError("Missing secret id")
    return SecretManagerConfig(project_id=project_id, secret_id=secret_id, version_id=version_id)


def create_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_resource_name(config: SecretManagerConfig) -> str:
    return f"projects/{config.project_id}/secrets/{config.secret_id}/versions/{config.version_id}"


def access_secret(config: Optional[SecretManagerConfig] = None, client: Optional[secretmanager.SecretManagerServiceClient] = None) -> str:
    config = config or load_config()
    client = client or create_client()
    response = client.access_secret_version(name=secret_resource_name(config))
    return response.payload.data.decode("utf-8")


def access_secret_json(config: Optional[SecretManagerConfig] = None, client: Optional[secretmanager.SecretManagerServiceClient] = None) -> Dict[str, Any]:
    import json

    return json.loads(access_secret(config=config, client=client))


def get_local_config() -> Dict[str, str]:
    config = load_config()
    return {
        "project_id": config.project_id,
        "secret_id": config.secret_id,
        "version_id": config.version_id,
    }
