import os
from google.cloud import secretmanager

def fetch_api_key(secret_id: str, project_id: str = None) -> str:
    """Fetches an API key from Google Secret Manager.
    
    Args:
        secret_id: The ID of the secret to fetch.
        project_id: The Google Cloud project ID. If None, it will be inferred.
    
    Returns:
        The API key as a string.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id
    # secret_id = "my-api-key-secret"
    # api_key = fetch_api_key(secret_id)
    # print(f"Fetched API Key: {api_key}")
    pass
