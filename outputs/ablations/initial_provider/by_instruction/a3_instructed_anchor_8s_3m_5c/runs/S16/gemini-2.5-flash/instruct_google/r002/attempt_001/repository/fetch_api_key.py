import os
from security_client import SecurityClient

def fetch_api_key(project_id: str, secret_id: str) -> str:
    client = SecurityClient()
    api_key_payload = client.access_secret_version(project_id, secret_id)
    return api_key_payload.data.decode('utf-8')

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    api_key_secret_id = "my-api-key"
    # In a real application, you would handle the API key securely.
    # For this example, we'll just print it.
    # print(f"Fetched API Key: {fetch_api_key(project_id, api_key_secret_id)}")
