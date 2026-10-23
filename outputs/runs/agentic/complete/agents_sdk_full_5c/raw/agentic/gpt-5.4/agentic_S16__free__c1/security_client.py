from __future__ import annotations

import os
from typing import Optional

from google.cloud import secretmanager
from google.cloud.secretmanager_v1 import SecretManagerServiceClient
from openai import OpenAI


DEFAULT_GCP_PROJECT_ENV = "GCP_PROJECT_ID"
DEFAULT_SECRET_NAME_ENV = "GCP_SECRET_ID"
DEFAULT_SECRET_VERSION_ENV = "GCP_SECRET_VERSION"
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


class SecretManagementConfig:
    def __init__(
        self,
        project_id: Optional[str] = None,
        secret_id: Optional[str] = None,
        version_id: Optional[str] = None,
    ) -> None:
        self.project_id = project_id or os.environ[DEFAULT_GCP_PROJECT_ENV]
        self.secret_id = secret_id or os.environ.get(DEFAULT_SECRET_NAME_ENV, "application-secret")
        self.version_id = version_id or os.environ.get(DEFAULT_SECRET_VERSION_ENV, "latest")

    @property
    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_id}/versions/{self.version_id}"



def get_secret_manager_client() -> SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()



def access_secret_version(resource_name: str) -> secretmanager.AccessSecretVersionResponse:
    client = get_secret_manager_client()
    return client.access_secret_version(request={"name": resource_name})



def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV])
