import os
from google.cloud import secretmanager


def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """Read a specific version (or staged) secret value from Google Cloud Secret Manager.

    Args:
        project_id (str): Google Cloud project identifier.
        secret_id (str): Secret ID to rotate.
        version_id (str): Version ID or 'latest' to read a specific version.

    Returns:
        str: The secret payload as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    # Construct the full version name
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
