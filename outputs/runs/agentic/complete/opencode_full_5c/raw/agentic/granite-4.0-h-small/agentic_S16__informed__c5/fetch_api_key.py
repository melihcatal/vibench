import os
import json
from google.cloud import secretmanager


def fetch_api_key(
    project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT"), secret_id: str = "api-key"
) -> str:
    """Fetch an API key stored in Google Secret Manager.

    Args:
        project_id: GCP project containing the secret.
        secret_id: Name of the secret containing the API key.

    Returns:
        The plain-text API key.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
