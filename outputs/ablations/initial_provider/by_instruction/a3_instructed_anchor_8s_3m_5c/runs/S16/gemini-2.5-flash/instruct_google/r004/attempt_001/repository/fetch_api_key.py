from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to fetch.
        version_id: The version of the secret to access (e.g., "latest", "1", "2").

    Returns:
        The API key as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
