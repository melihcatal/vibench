from google.cloud import secretmanager
import os

def fetch_api_key(project_id: str, secret_id: str) -> str:
    """Fetches an API key from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    api_key_secret_id = os.environ.get("API_KEY_SECRET_ID", "my-api-key")
    try:
        api_key = fetch_api_key(project_id, api_key_secret_id)
        print(f"Fetched API Key: {api_key[:5]}...") # Print first 5 chars for security
    except Exception as e:
        print(f"Error fetching API key: {e}")
