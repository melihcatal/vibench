import os
from dataclasses import dataclass

from google.cloud import secretmanager


@dataclass
class SecretManagerConfig:
    project_id: str
    secret_id: str
    version: str = "latest"


def load_config(project_env: str = "GOOGLE_CLOUD_PROJECT", secret_env: str = "SECRET_ID", version_env: str = "SECRET_VERSION") -> SecretManagerConfig:
    return SecretManagerConfig(
        project_id=os.environ[project_env],
        secret_id=os.environ[secret_env],
        version=os.getenv(version_env, "latest"),
    )


def client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_version_path(config: SecretManagerConfig) -> str:
    return f"projects/{config.project_id}/secrets/{config.secret_id}/versions/{config.version}"


def secret_path(config: SecretManagerConfig) -> str:
    return f"projects/{config.project_id}/secrets/{config.secret_id}"
