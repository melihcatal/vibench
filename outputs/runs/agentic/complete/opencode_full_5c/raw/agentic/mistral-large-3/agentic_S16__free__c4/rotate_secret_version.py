import os
from security_client import GoogleSecretManagerClient
from security_models import SecretResponse, normalize_secret_payload


def rotate_secret_version(secret_id: str, version_id: str) -> SecretResponse:
    client = GoogleSecretManagerClient()
    secret_data = client.get_secret_with_metadata(secret_id, version_id)
    return normalize_secret_payload(secret_data)
