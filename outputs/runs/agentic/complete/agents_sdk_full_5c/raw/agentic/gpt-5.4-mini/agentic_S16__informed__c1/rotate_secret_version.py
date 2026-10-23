from __future__ import annotations

from security_client import fetch_secret_value
from security_models import SecretRequest


def rotate_secret_version(secret_name: str, version_id: str | None = None, version_stage: str | None = None) -> str:
    response = fetch_secret_value(SecretRequest(name=secret_name, version_id=version_id, version_stage=version_stage))
    return response.value
