from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from google.cloud import secretmanager


@dataclass(frozen=True)
class SecretManagerConfig:
    project_id: str
    default_secret_name: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SecretManagerConfig":
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GOOGLE_PROJECT_ID")
        if not project_id:
            raise EnvironmentError("GOOGLE_CLOUD_PROJECT or GOOGLE_PROJECT_ID is required")
        return cls(project_id=project_id, default_secret_name=os.environ.get("SECRET_NAME"))


class SecretManagerClientHelper:
    def __init__(self, config: Optional[SecretManagerConfig] = None) -> None:
        self.config = config or SecretManagerConfig.from_env()
        self.client = secretmanager.SecretManagerServiceClient()

    def secret_path(self, secret_name: str, version: str = "latest") -> str:
        return self.client.secret_version_path(self.config.project_id, secret_name, version)

    def access_secret(self, secret_name: Optional[str] = None, version: str = "latest") -> str:
        name = secret_name or self.config.default_secret_name
        if not name:
            raise ValueError("secret_name is required")
        response = self.client.access_secret_version(request={"name": self.secret_path(name, version)})
        return response.payload.data.decode("utf-8")

    def get_secret_metadata(self, secret_name: str) -> Any:
        return self.client.get_secret(request={"name": self.client.secret_path(self.config.project_id, secret_name)})
