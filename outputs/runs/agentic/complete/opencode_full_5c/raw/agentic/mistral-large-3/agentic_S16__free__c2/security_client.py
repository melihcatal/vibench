from google.cloud import secretmanager
import os


class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    def get_secret_version(self, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def get_secret_version_metadata(self, secret_id: str, version_id: str) -> dict:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.get_secret_version(request={"name": name})
        return {
            "name": response.name,
            "create_time": response.create_time,
            "state": response.state.name,
            "etag": response.etag,
        }

    def list_secret_versions(self, secret_id: str) -> list:
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        response = self.client.list_secret_versions(request={"parent": parent})
        return [
            {"name": version.name, "state": version.state.name} for version in response
        ]

    def add_secret_version(self, secret_id: str, payload: str) -> dict:
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        response = self.client.add_secret_version(
            request={"parent": parent, "payload": {"data": payload.encode("UTF-8")}}
        )
        return {"name": response.name, "state": response.state.name}
