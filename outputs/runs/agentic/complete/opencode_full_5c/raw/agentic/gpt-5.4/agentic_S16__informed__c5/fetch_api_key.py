from __future__ import annotations

from security_client import get_secret_manager_client
from security_models import SecretRequest, normalize_secret_response


def fetch_api_key(request: SecretRequest):
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id)
    return normalize_secret_response(request.secret_id, response)
