from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str) -> str:
    """Fetches a database connection secret from Google Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to fetch.

    Returns:
        The database connection secret as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
