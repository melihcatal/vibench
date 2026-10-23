import os
from security_client import GoogleSecretManagerClient


def fetch_api_key(secret_id: str = "API_KEY") -> str:
    client = GoogleSecretManagerClient()
    api_key = client.get_secret(secret_id)
    return api_key
