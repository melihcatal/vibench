from google.cloud import secretmanager
import os


def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret to fetch.
        version_id: Version of the secret (defaults to "latest").

    Returns:
        The API key as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
