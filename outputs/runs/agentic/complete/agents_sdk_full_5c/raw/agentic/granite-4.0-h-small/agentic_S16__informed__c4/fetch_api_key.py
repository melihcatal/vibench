import os
from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str, version: str = "latest") -> str:
    """Fetches an API key secret from Google Secret Manager.

    Args:
        project_id: GCP project identifier.
        secret_id: Identifier of the secret containing the API key.
        version: Specific version to retrieve (default 'latest').

    Returns:
        The plain text API key.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8').strip()  # type: ignore
