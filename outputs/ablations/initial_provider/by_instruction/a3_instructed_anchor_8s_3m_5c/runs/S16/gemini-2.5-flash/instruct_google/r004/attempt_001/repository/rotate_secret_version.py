from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Accesses a specific secret version from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to access.
        version_id: The version of the secret to access (e.g., "latest", "1", "2").

    Returns:
        The secret payload as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def disable_secret_version(project_id: str, secret_id: str, version_id: str) -> None:
    """
    Disables a specific secret version in Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The version of the secret to disable.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    client.disable_secret_version(request={"name": name})

def destroy_secret_version(project_id: str, secret_id: str, version_id: str) -> None:
    """
    Destroys a specific secret version in Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The version of the secret to destroy.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    client.destroy_secret_version(request={"name": name})
