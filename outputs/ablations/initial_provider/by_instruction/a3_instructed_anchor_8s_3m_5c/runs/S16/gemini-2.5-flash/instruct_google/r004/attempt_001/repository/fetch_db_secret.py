from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches a database connection secret from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to fetch.
        version_id: The version of the secret to access (e.g., "latest", "1", "2").

    Returns:
        The database secret as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
