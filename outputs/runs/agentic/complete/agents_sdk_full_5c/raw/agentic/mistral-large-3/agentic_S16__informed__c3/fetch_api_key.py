import os
from security_client import get_secret_manager_client

def fetch_api_key(secret_name: str) -> str:
    """
    Fetch an API key from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    response = client.access_secret_version(request={
        "name": f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_name}/versions/latest"
    })
    return response.payload.data.decode("UTF-8")