import os
from google.cloud import secretmanager
from typing import Optional, Dict, Any

from security_models import SecretPayload, Secret


class SecretManagerClient:
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID must be set in environment or provided.")
        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret_version(
        self, secret_id: str, version_id: str = "latest"
    ) -> Secret:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        payload_data = response.payload.data
        return Secret(
            name=response.name,
            project_id=self.project_id,
            secret_id=secret_id,
            version_id=version_id,
            payload=SecretPayload(data=payload_data),
            labels=response.labels,
            annotations=response.annotations,
        )

    def add_secret_version(self, secret_id: str, payload_data: bytes) -> str:
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        response = self.client.add_secret_version(
            request={"parent": parent, "payload": {"data": payload_data}}
        )
        return response.name

    def destroy_secret_version(self, secret_id: str, version_id: str) -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.destroy_secret_version(request={"name": name})
        return response.name
