from __future__ import annotations

from security_client import secrets_manager_client
from security_models import SecretRequest, normalize_secret_value, text_from_secret


def fetch_api_key(request: SecretRequest, region_name: str | None = None) -> str:
    client = secrets_manager_client(region_name)
    response = client.get_secret_value(SecretId=request.secret_id)
    secret = normalize_secret_value(request.secret_id, response)
    return text_from_secret(secret)
