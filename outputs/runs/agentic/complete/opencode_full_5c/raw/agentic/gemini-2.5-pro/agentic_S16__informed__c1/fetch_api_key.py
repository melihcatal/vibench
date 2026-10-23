import os
from security_client import get_secrets_manager_client


def fetch_api_key(secret_name: str) -> str:
    """
    Fetches an API key from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return get_secret_value_response["SecretString"]
    except Exception as e:
        print(f"Error fetching secret {secret_name}: {e}")
        return None


if __name__ == "__main__":
    api_key_secret_name = os.environ.get("API_KEY_SECRET_NAME")
    if api_key_secret_name:
        api_key = fetch_api_key(api_key_secret_name)
        if api_key:
            print(f"Successfully fetched API key from secret: {api_key_secret_name}")
    else:
        print("Please set the API_KEY_SECRET_NAME environment variable.")
