from __future__ import annotations

from security_client import fetch_secret_value, parse_secret_json
from security_models import normalize_secret_payload


def fetch_db_secret(secret_id: str) -> dict:
    payload = fetch_secret_value(secret_id=secret_id, version_stage="AWSCURRENT")
    parsed = parse_secret_json(payload)
    return normalize_secret_payload(parsed)
