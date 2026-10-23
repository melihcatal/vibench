import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional

from google.cloud import secretmanager


@dataclass(frozen=True)
class SecretManagerConfig:
    project_id: str
    secret_id: str
    version: str = "latest"

    @classmethod
    def from_env(
        cls,
        *,
        secret_id_env: str,
        version_env: Optional[str] = None,
        project_envs: tuple[str, ...] = ("GOOGLE_CLOUD_PROJECT", "GCP_PROJECT"),
        default_version: str = "latest",
    ) -> "SecretManagerConfig":
        project_id = next((os.environ.get(name) for name in project_envs if os.environ.get(name)), None)
        secret_id = os.environ.get(secret_id_env)
        if not project_id or not secret_id:
            raise ValueError(f"{secret_id_env} and a Google Cloud project environment variable are required")
        version = os.environ.get(version_env, default_version) if version_env else default_version
        return cls(project_id=project_id, secret_id=secret_id, version=version)


def build_secret_name(project_id: str, secret_id: str, version: str = "latest") -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def create_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def access_secret_payload(
    client: Optional[secretmanager.SecretManagerServiceClient],
    config: SecretManagerConfig,
) -> str:
    sm_client = client or create_secret_manager_client()
    response = sm_client.access_secret_version(request={"name": build_secret_name(config.project_id, config.secret_id, config.version)})
    return response.payload.data.decode("utf-8")


def normalize_secret_text(payload: str) -> str:
    return payload.strip()


def load_secret_value(
    config: SecretManagerConfig,
    client: Optional[secretmanager.SecretManagerServiceClient] = None,
) -> str:
    return normalize_secret_text(access_secret_payload(client, config))


def config_from_mapping(mapping: Mapping[str, Any], *, default_version: str = "latest") -> SecretManagerConfig:
    project_id = mapping.get("project_id") or mapping.get("GOOGLE_CLOUD_PROJECT") or mapping.get("GCP_PROJECT")
    secret_id = mapping.get("secret_id")
    version = mapping.get("version") or default_version
    if not project_id or not secret_id:
        raise ValueError("project_id and secret_id are required")
    return SecretManagerConfig(project_id=str(project_id), secret_id=str(secret_id), version=str(version))
