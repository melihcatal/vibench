import os
from security_client import SecretManagerClient
from security_models import Secret


def fetch_api_key(secret_id: str, project_id: str = None) -> Secret:
    client = SecretManagerClient(project_id=project_id)
    api_key_secret = client.access_secret_version(secret_id=secret_id)
    return api_key_secret
