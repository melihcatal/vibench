import json

from security_client import get_secret_manager_client
from security_models import SecretFetchRequest, normalize_json_secret


def parse_json_secret(secret_name: str, version: str = "latest"):
    client = get_secret_manager_client()
    secret = client.fetch_secret(SecretFetchRequest(secret_name=secret_name, version=version))
    return normalize_json_secret(secret.value)
