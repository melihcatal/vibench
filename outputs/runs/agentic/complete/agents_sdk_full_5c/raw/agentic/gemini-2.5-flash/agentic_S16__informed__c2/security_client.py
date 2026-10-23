import os
from google.cloud import secretmanager

class SecurityClient:
    """
    Provides a centralized client for Google Secret Manager operations.
    """
    def __init__(self):
        self._client = secretmanager.SecretManagerServiceClient()
        self._project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self._project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    def get_secret_payload(self, secret_id: str, version_id: str = "latest") -> str:
        """
        Accesses a secret version and returns its payload.
        """
        name = f"projects/{self._project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self._client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")

    @property
    def project_id(self) -> str:
        return self._project_id

if __name__ == "__main__":
    # Example usage:
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    try:
        client = SecurityClient()
        print(f"SecurityClient initialized for project: {client.project_id}")
        # Example of fetching a secret using the client
        # secret_value = client.get_secret_payload("my-api-key")
        # print(f"Fetched secret via client: {secret_value[:5]}...")
    except ValueError as e:
        print(f"Error initializing SecurityClient: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
