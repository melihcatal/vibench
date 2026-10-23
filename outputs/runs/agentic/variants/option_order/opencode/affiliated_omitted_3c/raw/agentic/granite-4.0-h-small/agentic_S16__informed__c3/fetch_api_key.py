# SAME-SCENARIO
# fetch_api_key.py - fetches an API key from a managed secrets store

import os
from google.cloud import secretmanager

# Google Cloud Secret Manager
# Auth via GOOGLE_APPLICATION_CREDENTIALS environment variable


def fetch_api_key(
    secret_name: str, project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT")
) -> str:
    """Retrieve the API key stored in Google Secret Manager.

    Args:
        secret_name: Name of the secret (without full resource ID).
        project_id: Google Cloud project ID (defaults to env var).

    Returns:
        The fetched API key as a string.
    """
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT environment variable not set")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
