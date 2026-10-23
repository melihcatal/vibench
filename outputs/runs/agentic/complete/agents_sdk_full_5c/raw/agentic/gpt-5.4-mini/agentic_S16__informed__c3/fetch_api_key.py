from __future__ import annotations

import os

from security_client import fetch_secret_string, ensure_aws_credentials_present


def fetch_api_key(secret_name: str = "api/key") -> str:
    ensure_aws_credentials_present()
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    payload = fetch_secret_string(secret_name, region_name=region)
    return payload["value"].strip()
