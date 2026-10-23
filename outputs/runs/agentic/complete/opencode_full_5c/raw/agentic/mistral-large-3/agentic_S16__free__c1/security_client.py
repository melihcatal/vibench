from google.cloud import secretmanager
import os


class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    def get_secret_version(self, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def get_secret_latest_version(self, secret_id: str) -> str:
        return self.get_secret_version(secret_id, "latest")

    def list_secret_versions(self, secret_id: str):
        name = f"projects/{self.project_id}/secrets/{secret_id}"
        versions = self.client.list_secret_versions(request={"parent": name})
        return [version.name.split("/")[-1] for version in versions]

    def get_secret_with_metadata(
        self, secret_id: str, version_id: str = "latest"
    ) -> dict:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return {
            "payload": response.payload.data.decode("UTF-8"),
            "name": response.name,
            "create_time": response.create_time,
            "state": response.state.name,
        }
