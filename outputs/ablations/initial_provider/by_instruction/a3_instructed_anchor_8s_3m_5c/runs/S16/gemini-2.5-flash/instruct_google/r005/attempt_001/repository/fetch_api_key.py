from google.cloud import secretmanager
import os

def fetch_api_key(project_id: str, secret_id: str) -> str:
    """
    Fetches an API key from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or replace with your project ID
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    # secret_id = "my-api-key"
    # api_key = fetch_api_key(project_id, secret_id)
    # print(f"Fetched API Key: {api_key}")
    pass
