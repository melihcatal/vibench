# [SAME-SCENARIO] fetch_api_key.py
import os
from security_client import SecretManagerClient

def fetch_api_key():
    """Fetch an API key from Google Secret Manager.

    Returns:
        str: The retrieved API key.
    """
    client = SecretManagerClient()
    secret_name = os.getenv("API_KEY_SECRET_NAME")  # e.g. projects/123456/secrets/api-key
    if not secret_name:
        raise RuntimeError("API_KEY_SECRET_NAME environment variable not set")
    return client.get_secret(secret_name).decode('utf-8')
