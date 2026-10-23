import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import secretmanager


@dataclass(frozen=True)
class SecretManagerConfig:
    project_id: str
    secret_id: str
    version_id: str = "latest"


def load_config(
    secret_id: Optional[str] = None,
    project_id: Optional[str] = None,
    version_id: Optional[str] = None,
) -> SecretManagerConfig:
    resolved_secret_id = secret_id or os.environ.get("GOOGLE_SECRET_MANAGER_SECRET_ID")
    if not resolved_secret_id:
        raise ValueError("secret_id is required or must be set via GOOGLE_SECRET_MANAGER_SECRET_ID")

    resolved_project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not resolved_project_id:
        raise ValueError("project_id is required or must be set via GOOGLE_CLOUD_PROJECT/GCP_PROJECT")

    resolved_version_id = version_id or os.environ.get("GOOGLE_SECRET_MANAGER_SECRET_VERSION", "latest")
    return SecretManagerConfig(
        project_id=resolved_project_id,
        secret_id=resolved_secret_id,
        version_id=resolved_version_id,
    )


@lru_cache(maxsize=1)
def get_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def build_secret_name(config: SecretManagerConfig) -> str:
    return f"projects/{config.project_id}/secrets/{config.secret_id}/versions/{config.version_id}"


def read_secret(
    secret_id: Optional[str] = None,
    project_id: Optional[str] = None,
    version_id: Optional[str] = None,
) -> str:
    config = load_config(secret_id=secret_id, project_id=project_id, version_id=version_id)
    response = get_client().access_secret_version(request={"name": build_secret_name(config)})
    return response.payload.data.decode("utf-8")


def get_secret_client(secret_id: Optional[str] = None, project_id: Optional[str] = None, version_id: Optional[str] = None):
    config = load_config(secret_id=secret_id, project_id=project_id, version_id=version_id)
    return get_client(), build_secret_name(config)
