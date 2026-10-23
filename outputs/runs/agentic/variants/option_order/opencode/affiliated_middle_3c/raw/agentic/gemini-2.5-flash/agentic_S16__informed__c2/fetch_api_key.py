import os
from security_client import SecretManagerClient
from security_models import SecretRequest


def fetch_api_key(project_id: str, secret_id: str) -> str:
    client = SecretManagerClient()
    request = SecretRequest(project_id=project_id, secret_id=secret_id)
    response = client.access_secret_version(request)
    return response.payload


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    api_key_secret_id = "my-api-key"
    if project_id:
        api_key = fetch_api_key(project_id, api_key_secret_id)
        print(f"Fetched API Key: {api_key}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
