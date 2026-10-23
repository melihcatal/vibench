from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str) -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")
