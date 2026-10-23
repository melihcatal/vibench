import os
from google.cloud import secretmanager

class SecretManagerClient:
    """A simple client helper for Google Secret Manager."""
    def __init__(self, project_id: str = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT env var.")
        self._client = secretmanager.SecretManagerServiceClient()

    def get_secret_payload(self, secret_id: str, version_id: str = "latest") -> str:
        """Accesses the payload of a specific secret version."""
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self._client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    def create_secret(self, secret_id: str, secret_data: str) -> str:
        """Creates a new secret and adds an initial version."""
        parent = f"projects/{self.project_id}"
        secret = {"replication": {"automatic": {}}}
        create_response = self._client.create_secret(request={"parent": parent, "secret_id": secret_id, "secret": secret})

        payload = secret_data.encode("UTF-8")
        add_version_response = self._client.add_secret_version(request={"parent": create_response.name, "payload": {"data": payload}})
        return add_version_response.name # Returns the name of the new secret version

if __name__ == "__main__":
    # Example usage
    try:
        sm_client = SecretManagerClient()
        # For demonstration, you might need to create a secret first
        # new_secret_version_name = sm_client.create_secret("my-test-secret", "my-test-value")
        # print(f"Created new secret version: {new_secret_version_name}")

        secret_value = sm_client.get_secret_payload("my-api-key-secret")
        print(f"Fetched secret via helper client.")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
