from security_client import SecretManagerClient
import os


def fetch_api_key(secret_id: str = "API_KEY") -> str:
    client = SecretManagerClient()
    api_key = client.get_secret_latest_version(secret_id)
    return api_key
