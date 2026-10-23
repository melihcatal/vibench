from __future__ import annotations

from security_client import fetch_secret_payload
from security_models import redact_secret_text


def fetch_api_key(secret_id: str) -> dict:
    payload = fetch_secret_payload(secret_id)
    return {
        "provider": "aws-secrets-manager",
        "secret_id": payload.secret_id,
        "version_id": payload.version_id,
        "api_key": payload.value,
        "masked_api_key": redact_secret_text(payload.value),
    }
