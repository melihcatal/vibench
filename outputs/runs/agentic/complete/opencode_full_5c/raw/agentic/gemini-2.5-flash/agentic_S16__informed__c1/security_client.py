import os
from google.cloud import secretmanager


class SecretManagerClient:
    """Client for interacting with Google Secret Manager."""

    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    def get_secret_path(self, secret_id: str, version_id: str = "latest") -> str:
        return self.client.secret_version_path(self.project_id, secret_id, version_id)

    def access_secret_version(self, secret_id: str, version_id: str = "latest") -> str:
        name = self.get_secret_path(secret_id, version_id)
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
