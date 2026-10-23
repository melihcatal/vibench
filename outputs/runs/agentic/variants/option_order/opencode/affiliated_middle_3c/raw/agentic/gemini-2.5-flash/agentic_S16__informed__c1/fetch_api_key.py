import os
from google.cloud import secretmanager


def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches an API key from Google Secret Manager.
    Provider: Google Cloud Secret Manager
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # secret_id = "my-api-key"
    # api_key = fetch_api_key(project_id, secret_id)
    # print(f"Fetched API Key: {api_key}")
    pass
