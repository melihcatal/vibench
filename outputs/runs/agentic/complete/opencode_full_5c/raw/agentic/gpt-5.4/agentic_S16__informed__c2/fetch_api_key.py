from __future__ import annotations

from security_client import get_secrets_manager_client
from security_models import SecretRequest, normalize_secret_response


def fetch_api_key(secret_id: str):
    request = SecretRequest(secret_id=secret_id)
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id)
    return normalize_secret_response(secret_id, response)
