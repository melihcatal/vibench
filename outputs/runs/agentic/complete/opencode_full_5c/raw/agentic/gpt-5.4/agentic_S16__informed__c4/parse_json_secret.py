from __future__ import annotations

from security_client import secrets_manager_client
from security_models import SecretRequest, normalize_secret_value, parse_secret_json


def parse_json_secret(request: SecretRequest, region_name: str | None = None) -> dict:
    client = secrets_manager_client(region_name)
    response = client.get_secret_value(SecretId=request.secret_id)
    secret = normalize_secret_value(request.secret_id, response)
    return parse_secret_json(secret)
