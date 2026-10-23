import os
import json
from security_client import SecretsManagerClient


def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key stored as a secret in a managed secrets store.

    Args:
        secret_name: Name of the secret containing the API key.

    Returns:
        The retrieved API key as a string.
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(name=secret_name)
    # Assume secret value is stored as plain text
    return response["SecretString"]


if __name__ == "__main__":
    # Example usage
    api_key = fetch_api_key(os.getenv("API_KEY_SECRET_NAME"))
    print(f"Fetched API Key: {api_key}")
