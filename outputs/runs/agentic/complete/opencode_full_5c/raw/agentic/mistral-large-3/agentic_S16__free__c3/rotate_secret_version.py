from google.cloud import secretmanager
import os


def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Reads a specific secret version or staged value from Google Cloud Secret Manager.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret to fetch.
        version_id: Version of the secret to fetch.

    Returns:
        The secret value as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
