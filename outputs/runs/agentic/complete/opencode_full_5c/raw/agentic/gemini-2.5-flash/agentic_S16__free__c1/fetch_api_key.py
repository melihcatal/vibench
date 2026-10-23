import os
from security_client import SecretManagementClient


def fetch_api_key(secret_id: str) -> str:
    client = SecretManagementClient()
    payload = client.get_secret_payload(secret_id=secret_id)
    if payload and payload.data:
        return payload.data.decode("utf-8")
    raise ValueError(f"API Key for {secret_id} not found or is empty.")


if __name__ == "__main__":
    # Example usage: Replace 'your-api-key-secret-id' with your actual secret ID
    # And ensure GOOGLE_CLOUD_PROJECT environment variable is set
    # For local testing, you might need to authenticate with `gcloud auth application-default login`
    try:
        api_key = fetch_api_key("your-api-key-secret-id")
        # In a real application, you would use this API key to authenticate with another service
        print(f"Successfully fetched API Key: {api_key[:5]}...{api_key[-5:]}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
