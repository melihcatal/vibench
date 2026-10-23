from __future__ import annotations

import os

from security_client import fetch_secret_string, ensure_aws_credentials_present
from security_models import extract_json_payload


def parse_json_secret(secret_name: str = "app/json") -> dict:
    ensure_aws_credentials_present()
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    payload = fetch_secret_string(secret_name, region_name=region)
    parsed = extract_json_payload(payload["value"])
    if isinstance(parsed, dict):
        return parsed
    return {"value": parsed}
