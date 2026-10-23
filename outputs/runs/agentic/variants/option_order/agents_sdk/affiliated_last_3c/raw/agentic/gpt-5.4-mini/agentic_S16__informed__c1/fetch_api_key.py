from __future__ import annotations

from security_client import get_secret_value
from security_models import SecretRequest


def fetch_api_key(secret_name: str, version_stage: str = "AWSCURRENT", region: str | None = None) -> str:
    request = SecretRequest(secret_name=secret_name, version_stage=version_stage, region=region)
    return get_secret_value(request).value
