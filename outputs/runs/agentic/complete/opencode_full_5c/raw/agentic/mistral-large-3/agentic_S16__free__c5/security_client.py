from google.cloud import secretmanager
import os


class SecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    def get_secret_version(self, secret_id, version_id="latest"):
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def get_secret_latest(self, secret_id):
        return self.get_secret_version(secret_id, "latest")

    def list_secret_versions(self, secret_id):
        name = f"projects/{self.project_id}/secrets/{secret_id}"
        response = self.client.list_secret_versions(request={"parent": name})
        return [version.name.split("/")[-1] for version in response]

    def add_secret_version(self, secret_id, payload):
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        response = self.client.add_secret_version(
            request={"parent": parent, "payload": {"data": payload.encode("UTF-8")}}
        )
        return response.name.split("/")[-1]
