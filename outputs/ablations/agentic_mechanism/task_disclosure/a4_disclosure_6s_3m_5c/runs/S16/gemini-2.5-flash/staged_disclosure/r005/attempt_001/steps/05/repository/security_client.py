import os
from google.cloud import secretmanager

class SecretManagerClient:
    """
    A client for managing secrets.
    This example uses Google Cloud Secret Manager.
    """
    def __init__(self):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        """
        Fetches a secret from Google Cloud Secret Manager.

        Args:
            secret_id: The ID of the secret to fetch.
            version_id: The version of the secret to fetch (e.g., "latest", "1").

        Returns:
            The secret payload as a string.
        """
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")

    # Add other secret management utilities here, e.g., create_secret, update_secret, etc.

# Example local configuration (can be moved to environment variables or a config file)
# In a real application, avoid hardcoding sensitive information.
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

if __name__ == "__main__":
    # This is an example of how to use the client.
    # In a real application, you would not hardcode secret_id here.
    # Ensure GOOGLE_CLOUD_PROJECT environment variable is set.
    try:
        secret_client = SecretManagerClient()
        # Replace 'my-test-secret' with an actual secret ID in your GCP project
        # secret_value = secret_client.get_secret("my-test-secret")
        # print(f"Successfully fetched secret: {secret_value}")
        print("SecretManagerClient initialized. To use, set GOOGLE_CLOUD_PROJECT and call get_secret().")
    except ValueError as e:
        print(f"Error: {e}. Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
