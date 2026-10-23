import os
from typing import Any, Dict

from security_client import SecretManagerClient, get_secret_manager_client
from security_models import SecretFetchRequest, SecretValue


def fetch_api_key(secret_name: str, version: str = "latest") -> SecretValue:
    client = get_secret_manager_client()
    request = SecretFetchRequest(secret_name=secret_name, version=version)
    return client.fetch_secret(request)
