from __future__ import annotations

from security_client import fetch_secret_value
from security_models import SecretRequest


def fetch_api_key(secret_name: str) -> str:
    response = fetch_secret_value(SecretRequest(name=secret_name))
    return response.value
