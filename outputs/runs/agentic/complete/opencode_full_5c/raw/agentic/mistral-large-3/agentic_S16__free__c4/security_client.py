import os
from google.cloud import secretmanager
from google.api_core.exceptions import GoogleAPICallError, NotFound, PermissionDenied


class GoogleSecretManagerClient:
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except (GoogleAPICallError, NotFound, PermissionDenied) as e:
            raise Exception(f"Failed to fetch secret {secret_id}: {str(e)}")

    def get_secret_version(self, secret_id: str, version_id: str) -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except (GoogleAPICallError, NotFound, PermissionDenied) as e:
            raise Exception(
                f"Failed to fetch secret {secret_id} version {version_id}: {str(e)}"
            )

    def get_secret_with_metadata(
        self, secret_id: str, version_id: str = "latest"
    ) -> dict:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return {
                "payload": response.payload.data.decode("UTF-8"),
                "name": response.name,
                "create_time": response.create_time,
                "state": response.state.name,
            }
        except (GoogleAPICallError, NotFound, PermissionDenied) as e:
            raise Exception(
                f"Failed to fetch secret {secret_id} with metadata: {str(e)}"
            )
