import os
from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches an API key from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    api_secret_id = "my-api-key" # Replace with your secret ID

    if project_id:
        try:
            api_key = fetch_api_key(project_id, api_secret_id)
            print(f"Successfully fetched API key (first 5 chars): {api_key[:5]}...")
        except Exception as e:
            print(f"Error fetching API key: {e}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
