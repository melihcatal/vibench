from __future__ import annotations

from security_client import fetch_secret_value
from security_models import normalize_secret_payload


def fetch_api_key(secret_id: str) -> dict:
    payload = fetch_secret_value(secret_id=secret_id, version_stage="AWSCURRENT")
    return normalize_secret_payload(payload)
