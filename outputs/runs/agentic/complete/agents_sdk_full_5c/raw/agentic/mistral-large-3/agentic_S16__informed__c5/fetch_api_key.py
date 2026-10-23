from google.cloud import secretmanager


def fetch_api_key(secret_id: str, project_id: str, version_id: str = "latest") -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.
    
    Args:
        secret_id: The ID of the secret to fetch.
        project_id: The Google Cloud project ID.
        version_id: The version of the secret to fetch (default: "latest").
        
    Returns:
        The secret value as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")