import os
from security_client import AWSSecretManagerClient


def fetch_api_key(secret_name: str) -> str:
    """Fetches an API key from AWS Secrets Manager."""
    client = AWSSecretManagerClient()
    try:
        get_secret_value_response = client.client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            return get_secret_value_response["SecretString"]
        else:
            raise ValueError("SecretString not found in response.")
    except Exception as e:
        print(f"Error fetching API key: {e}")
        raise
