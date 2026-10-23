from __future__ import annotations

from security_client import fetch_secret_payload
from security_models import parse_json_secret_value


def parse_json_secret(secret_id: str) -> dict:
    payload = fetch_secret_payload(secret_id)
    parsed = parse_json_secret_value(payload.value)
    return {
        "provider": "aws-secrets-manager",
        "secret_id": payload.secret_id,
        "version_id": payload.version_id,
        "data": parsed,
    }
