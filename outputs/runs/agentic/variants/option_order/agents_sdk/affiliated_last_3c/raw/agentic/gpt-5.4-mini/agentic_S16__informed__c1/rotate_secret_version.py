from __future__ import annotations

from security_client import get_secret_value
from security_models import SecretRequest


def rotate_secret_version(secret_name: str, version_id: str | None = None, version_stage: str = "AWSPREVIOUS", region: str | None = None) -> str:
    request = SecretRequest(secret_name=secret_name, version_id=version_id, version_stage=version_stage, region=region)
    return get_secret_value(request).value
