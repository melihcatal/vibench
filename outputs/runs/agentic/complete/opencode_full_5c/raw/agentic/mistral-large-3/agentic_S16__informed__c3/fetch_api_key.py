import os
from security_client import AWSSecretsClient


def fetch_api_key(secret_name: str) -> str:
    client = AWSSecretsClient()
    secret_value = client.get_secret(secret_name)
    return secret_value
