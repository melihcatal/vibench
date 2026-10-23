import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import secretmanager


@dataclass
class SecretClientConfig:
    project_id: str
    secret_name: str
    version: str = "latest"


def load_config(
    secret_name: str, version: str = "latest", project_id: Optional[str] = None
) -> SecretClientConfig:
    return SecretClientConfig(
        project_id=project_id or os.environ["GOOGLE_CLOUD_PROJECT"],
        secret_name=secret_name,
        version=version,
    )


def client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_path(cfg: SecretClientConfig) -> str:
    return f"projects/{cfg.project_id}/secrets/{cfg.secret_name}/versions/{cfg.version}"
