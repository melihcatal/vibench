from __future__ import annotations

import os

from security_client import env_secret_name, safe_fetch


def fetch_api_key(secret_id: str | None = None) -> str:
    secret = secret_id or env_secret_name("service/api-key").normalized()
    return safe_fetch(secret, region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
