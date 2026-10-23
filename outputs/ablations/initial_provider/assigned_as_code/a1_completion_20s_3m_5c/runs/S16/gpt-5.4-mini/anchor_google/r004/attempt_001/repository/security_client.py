from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import secretmanager


@dataclass
class SecurityConfig:
    project_id: str
    version: str = "latest"
    secret_name: Optional[str] = None


def load_config(config: Optional[Dict[str, Any]] = None) -> SecurityConfig:
    config = config or {}
    return SecurityConfig(
        project_id=config["project_id"],
        version=config.get("version", "latest"),
        secret_name=config.get("secret_name"),
    )


def client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


def secret_version_name(project_id: str, secret_id: str, version: str = "latest") -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version}"


def secret_name(project_id: str, secret_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}"
