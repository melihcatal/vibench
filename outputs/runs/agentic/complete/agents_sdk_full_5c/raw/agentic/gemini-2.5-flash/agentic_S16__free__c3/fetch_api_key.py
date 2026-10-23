import os
from google.cloud import secretmanager

def fetch_api_key(project_id: str, secret_id: str) -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.getenv("GCP_PROJECT_ID")
    api_key_secret_id = "my-api-key"
    if project_id:
        try:
            api_key = fetch_api_key(project_id, api_key_secret_id)
            print(f"Fetched API Key (first 5 chars): {api_key[:5]}*****")
        except Exception as e:
            print(f"Error fetching API key: {e}")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
