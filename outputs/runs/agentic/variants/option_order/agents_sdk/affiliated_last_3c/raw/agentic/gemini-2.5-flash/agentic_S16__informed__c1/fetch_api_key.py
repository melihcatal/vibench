import os
from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """Fetches an API key from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    api_secret_id = "my-api-key-secret"
    if project_id:
        try:
            api_key = fetch_api_key(project_id, api_secret_id)
            print(f"Successfully fetched API key.")
        except Exception as e:
            print(f"Error fetching API key: {e}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
