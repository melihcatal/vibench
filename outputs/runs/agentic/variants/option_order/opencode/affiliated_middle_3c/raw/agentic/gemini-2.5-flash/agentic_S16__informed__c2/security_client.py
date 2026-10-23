import os
from google.cloud import secretmanager
from security_models import SecretRequest, SecretResponse


class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication

    def access_secret_version(self, request: SecretRequest) -> SecretResponse:
        name = f"projects/{request.project_id}/secrets/{request.secret_id}/versions/{request.version_id}"
        response = self.client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return SecretResponse(
            name=response.name, payload=payload, version=request.version_id
        )

    def add_secret_version(
        self, project_id: str, secret_id: str, payload: str
    ) -> SecretResponse:
        parent = f"projects/{project_id}/secrets/{secret_id}"
        response = self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload.encode("UTF-8")},
            }
        )
        return SecretResponse(name=response.name, version=response.name.split("/")[-1])
