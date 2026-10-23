import os
from google.cloud import secretmanager
from typing import Optional

class SecretManagerClient:
    """
    A helper client for Google Cloud Secret Manager.
    Encapsulates client initialization and common project/secret ID parsing.
    """
    def __init__(self, project_id: Optional[str] = None):
        self._client = secretmanager.SecretManagerServiceClient()
        self._project_id = project_id if project_id else os.getenv("GCP_PROJECT_ID")
        if not self._project_id:
            raise ValueError("GCP_PROJECT_ID must be provided or set as an environment variable.")

    def get_secret_version_name(self, secret_id: str, version_id: str = "latest") -> str:
        """Constructs the full resource name for a secret version."""
        return f"projects/{self._project_id}/secrets/{secret_id}/versions/{version_id}"

    def access_secret_payload(self, secret_id: str, version_id: str = "latest") -> str:
        """Accesses a secret version and returns its payload."""
        name = self.get_secret_version_name(secret_id, version_id)
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def list_secrets(self, filter_str: Optional[str] = None):
        """Lists secrets in the project with an optional filter."""
        parent = f"projects/{self._project_id}"
        if filter_str:
            return self._client.list_secrets(request={"parent": parent, "filter": filter_str})
        return self._client.list_secrets(request={"parent": parent})

if __name__ == "__main__":
    # Example usage
    try:
        sm_client = SecretManagerClient()
        print("SecretManagerClient initialized successfully.")
        # Test accessing a dummy secret (replace with a real one for actual testing)
        # dummy_secret = sm_client.access_secret_payload("my-test-secret", "latest")
        # print(f"Accessed dummy secret: {dummy_secret[:5]}...")

        # Test listing secrets
        # print("\nListing secrets:")
        # for secret in sm_client.list_secrets():
        #     print(f"- {secret.name}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
