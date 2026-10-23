import os
from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """Reads a specific version (or staged) value of a secret from GCP Secret Manager.

    Args:
        project_id (str): GCP project ID.
        secret_id (str): Secret name.
        version_id (str): Version number or alias (e.g., 'latest', '1', 'staged').

    Returns:
        str: The secret payload for the requested version.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name)
    return response.payload.data.decode('UTF-8')
