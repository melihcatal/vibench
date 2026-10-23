from __future__ import annotations

from security_client import fetch_secret_value, parse_secret_json
from security_models import normalize_secret_payload


def parse_json_secret(secret_id: str, version_stage: str = "AWSCURRENT") -> dict:
    payload = fetch_secret_value(secret_id=secret_id, version_stage=version_stage)
    parsed = parse_secret_json(payload)
    return normalize_secret_payload(parsed)
