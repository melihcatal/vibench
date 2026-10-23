import os
from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str) -> str:
    """Fetches an API key from Google Secret Manager.

    Args:
        project_id (str): GCP project ID.
        secret_id (str): Secret name.

    Returns:
        str: The fetched API key.
    """
    # Configure the client using GOOGLE_APPLICATION_CREDENTIALS env var
    client = secretmanager.SecretManagerServiceClient()
    # Secret version format: projects/{project}/secrets/{secret}/versions/latest
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')
