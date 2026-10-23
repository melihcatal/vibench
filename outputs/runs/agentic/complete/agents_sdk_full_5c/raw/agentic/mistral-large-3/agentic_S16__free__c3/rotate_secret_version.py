import os
from google.cloud import secretmanager


def rotate_secret_version(secret_id: str, project_id: str = None, version_id: str = "latest") -> str:
    """
    Reads a specific secret version or staged value from Google Cloud Secret Manager.
    
    Args:
        secret_id: The secret ID (e.g., "my-secret").
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
        version_id: The version ID (e.g., "1" or "latest").
    
    Returns:
        The secret value as a string.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")