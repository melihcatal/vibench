import os
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound
from security_models import SecretPayload, SecretVersion, Secret


class SecretManagementClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret_payload(
        self, secret_id: str, version_id: str = "latest"
    ) -> Optional[SecretPayload]:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return SecretPayload(
                data=response.payload.data, data_crc32c=response.payload.data_crc32c
            )
        except NotFound:
            return None

    def get_secret_metadata(self, secret_id: str) -> Optional[Secret]:
        name = f"projects/{self.project_id}/secrets/{secret_id}"
        try:
            response = self.client.get_secret(request={"name": name})
            return Secret(
                name=response.name,
                labels=response.labels,
                create_time=response.create_time,
            )
        except NotFound:
            return None

    def list_secret_versions(self, secret_id: str) -> list[SecretVersion]:
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        versions = []
        for version in self.client.list_secret_versions(request={"parent": parent}):
            versions.append(
                SecretVersion(
                    name=version.name,
                    state=version.state,
                    create_time=version.create_time,
                )
            )
        return versions

    def add_secret_version(self, secret_id: str, payload: bytes) -> SecretVersion:
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        response = self.client.add_secret_version(
            request={
                "parent": parent,
                "payload": {"data": payload},
            }
        )
        return SecretVersion(
            name=response.name, state=response.state, create_time=response.create_time
        )

    def destroy_secret_version(self, secret_version_name: str):
        self.client.destroy_secret_version(request={"name": secret_version_name})
