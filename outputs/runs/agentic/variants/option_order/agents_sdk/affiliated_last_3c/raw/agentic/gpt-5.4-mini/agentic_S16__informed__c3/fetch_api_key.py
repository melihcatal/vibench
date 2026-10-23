from __future__ import annotations

from security_client import SecurityClient
from security_models import SecretRequest

AWS_SECRET_NAME = "prod/api/key"


def fetch_api_key(secret_name: str = AWS_SECRET_NAME) -> str:
    client = SecurityClient()
    return client.get_secret_text(SecretRequest(name=secret_name))
