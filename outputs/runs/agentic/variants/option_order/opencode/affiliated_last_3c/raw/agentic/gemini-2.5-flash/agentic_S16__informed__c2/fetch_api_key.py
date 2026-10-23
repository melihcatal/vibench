import os
from google.cloud import secretmanager_v1 as secretmanager


def fetch_api_key(secret_id: str, version_id: str = "latest") -> str:
    """Fetches an API key from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    name = client.secret_version_path(project_id, secret_id, version_id)
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
