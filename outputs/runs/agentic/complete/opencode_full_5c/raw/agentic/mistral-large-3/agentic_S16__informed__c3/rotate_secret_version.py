import os
from security_client import AWSSecretsClient


def rotate_secret_version(secret_name: str, version_id: str) -> str:
    client = AWSSecretsClient()
    secret_value = client.get_secret_version(secret_name, version_id)
    return secret_value
