from google.cloud import secretmanager

class SecretManagerClient:
    """A client helper for Google Secret Manager operations."""

    def __init__(self):
        self._client = secretmanager.SecretManagerServiceClient()

    def access_secret(self, project_id: str, secret_id: str, version_id: str = "latest") -> str:
        """Accesses a secret version.

        Args:
            project_id: The Google Cloud project ID.
            secret_id: The ID of the secret.
            version_id: The specific version of the secret to access.

        Returns:
            The secret payload as a string.
        """
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
