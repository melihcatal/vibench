from __future__ import annotations

from security_client import parse_json_secret as _parse_json_secret, safe_get_secret
from security_models import SecretRequest

# AWS Secrets Manager integration
SECRET_ID = "app/config/json"


def parse_json_secret() -> dict:
    req = SecretRequest(secret_id=SECRET_ID)
    response = safe_get_secret(req.secret_id)
    return _parse_json_secret(response)
