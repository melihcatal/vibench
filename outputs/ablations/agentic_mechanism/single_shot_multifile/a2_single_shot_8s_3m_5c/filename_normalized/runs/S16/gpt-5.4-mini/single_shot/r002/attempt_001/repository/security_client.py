import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import secretmanager

from security_models import SecretFetchRequest, SecretValue, SecretVersionRequest, normalize_secret_payload


@dataclass
class SecretManagerConfig:
    project_id: str


def load_config() -> SecretManagerConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT must be set")
    return SecretManagerConfig(project_id=project_id)


class SecretManagerClient:
    def __init__(self, config: Optional[SecretManagerConfig] = None):
        self.config = config or load_config()
        self.client = secretmanager.SecretManagerServiceClient()

    def _build_name(self, secret_name: str, version: str) -> str:
        return f"projects/{self.config.project_id}/secrets/{secret_name}/versions/{version}"

    def fetch_secret(self, request: SecretFetchRequest) -> SecretValue:
        name = self._build_name(request.secret_name, request.version)
        response = self.client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("utf-8")
        return SecretValue(secret_name=request.secret_name, version=request.version, value=payload, normalized=normalize_secret_payload(payload))

    def fetch_secret_version(self, request: SecretVersionRequest) -> SecretValue:
        version = request.stage if request.stage else request.version
        return self.fetch_secret(SecretFetchRequest(secret_name=request.secret_name, version=version))


def get_secret_manager_client() -> SecretManagerClient:
    return SecretManagerClient()
