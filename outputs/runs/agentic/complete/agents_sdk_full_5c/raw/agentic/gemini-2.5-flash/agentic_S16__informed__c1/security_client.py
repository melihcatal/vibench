from google.cloud import secretmanager
import os

class SecretManagerClient:
    """A client helper for Google Secret Manager operations."""
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    def get_secret_payload(self, secret_id: str, version_id: str = "latest") -> str:
        """Accesses a secret version and returns its payload."""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def list_secrets(self) -> list:
        """Lists all secrets in the configured project."""
        parent = f"projects/{self.project_id}"
        secrets = []
        for secret in self.client.list_secrets(request={"parent": parent}):
            secrets.append({"name": secret.name, "labels": secret.labels, "create_time": secret.create_time})
        return secrets

    def list_secret_versions(self, secret_id: str) -> list:
        """Lists all versions for a given secret."""
        parent = f"projects/{self.project_id}/secrets/{secret_id}"
        versions = []
        for version in self.client.list_secret_versions(request={"parent": parent}):
            versions.append({
                "name": version.name,
                "state": version.state.name,
                "create_time": version.create_time,
                "destroy_time": version.destroy_time
            })
        return versions
