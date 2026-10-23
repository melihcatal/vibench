import os
from security_client import get_secrets_manager_client


def fetch_api_key(secret_id: str) -> str:
    """
    Fetches a simple API key from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_id)
        return response.get("SecretString", "")
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret with ID '{secret_id}' not found.")
        return ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


if __name__ == "__main__":
    api_key_secret_id = os.environ.get("API_KEY_SECRET_ID", "my-app/api-key")
    api_key = fetch_api_key(api_key_secret_id)
    if api_key:
        print(f"Successfully fetched API key from secret: {api_key_secret_id}")
    else:
        print(f"Failed to fetch API key from secret: {api_key_secret_id}")
