import os
from security_client import SecretManagerHelper

# Google Cloud Project ID can be set as an environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


def fetch_api_key(secret_id: str) -> str:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = SecretManagerHelper(project_id=PROJECT_ID)
    secret_payload = client.get_secret_value(secret_id)
    return secret_payload.data.decode("utf-8")


# Example Usage (replace with actual secret_id and set GOOGLE_CLOUD_PROJECT_ID env var)
if __name__ == "__main__":
    try:
        api_key = fetch_api_key("my-api-key-secret")
        print(f"Fetched API Key: {api_key[:5]}...")  # Print first 5 chars for security
    except Exception as e:
        print(f"Error fetching API key: {e}")
