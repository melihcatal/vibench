from __future__ import annotations

from security_client import get_secret_manager_client
from security_models import SecretRequest, normalize_secret_response, parse_secret_json


def parse_json_secret(request: SecretRequest):
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id)
    secret = normalize_secret_response(request.secret_id, response)
    return parse_secret_json(secret.value)
