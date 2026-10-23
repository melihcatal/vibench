from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Reads a specific secret version or staged value from Google Cloud Secret Manager.
    This function is primarily for demonstrating access to a specific version.
    Actual rotation would involve creating a new version.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
