from google.cloud import secretmanager
import os


def fetch_api_key(project_id: str, secret_id: str) -> str:
    """Fetches an API key from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    api_key_secret_id = os.environ.get("API_KEY_SECRET_ID", "my-api-key")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    key = fetch_api_key(project_id, api_key_secret_id)
    print(f"Fetched API Key: {key[:5]}...")  # Print a portion for security
