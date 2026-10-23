import os
from google.cloud import secretmanager

def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key from Google Secret Manager.
The secret must exist in the project associated with the credentials
set via GOOGLE_APPLICATION_CREDENTIALS environment variable."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')