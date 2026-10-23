from __future__ import annotations

import json
import os

from security_client import fetch_secret_string, ensure_aws_credentials_present
from security_models import extract_json_payload


def fetch_db_secret(secret_name: str = "database/connection") -> dict:
    ensure_aws_credentials_present()
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    payload = fetch_secret_string(secret_name, region_name=region)
    data = extract_json_payload(payload["value"])
    if isinstance(data, dict):
        return data
    return {"raw": json.dumps(data)}
