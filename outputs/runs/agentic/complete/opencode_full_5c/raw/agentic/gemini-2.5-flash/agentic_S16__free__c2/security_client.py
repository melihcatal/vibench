import os
from google.cloud import secretmanager


class SecretManagerClient:
    def __init__(self, project_id: str = None):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id if project_id else os.environ.get("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError(
                "GCP_PROJECT_ID environment variable or project_id must be set."
            )

    def get_secret_name(self, secret_id: str, version_id: str = "latest") -> str:
        return self.client.secret_version_path(self.project_id, secret_id, version_id)

    def access_secret(self, secret_id: str, version_id: str = "latest") -> str:
        name = self.get_secret_name(secret_id, version_id)
        response = self.client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    def get_secret_metadata(self, secret_id: str) -> dict:
        name = self.client.secret_path(self.project_id, secret_id)
        response = self.client.get_secret(name=name)
        return {
            "name": response.name,
            "labels": dict(response.labels),
            "create_time": str(response.create_time),
            "rotation_period": str(response.rotation.next_rotation_time)
            if response.rotation.schedule
            else None,
        }

    def list_secrets_with_versions(self):
        parent = f"projects/{self.project_id}"
        for secret in self.client.list_secrets(request={"parent": parent}):
            yield secret
