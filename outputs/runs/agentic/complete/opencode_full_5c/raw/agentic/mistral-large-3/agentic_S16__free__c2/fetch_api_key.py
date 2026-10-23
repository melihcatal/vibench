from security_client import SecretManagerClient
import os


def fetch_api_key(service_name: str) -> str:
    client = SecretManagerClient()
    secret_id = f"{service_name}-api-key"
    return client.get_secret_version(secret_id=secret_id)
