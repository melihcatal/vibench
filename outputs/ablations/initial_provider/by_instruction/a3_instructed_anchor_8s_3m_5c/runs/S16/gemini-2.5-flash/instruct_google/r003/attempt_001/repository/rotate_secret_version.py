from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """Reads a specific secret version from Google Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The specific version of the secret to access (e.g., '1', '2', or 'latest').

    Returns:
        The secret payload as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
