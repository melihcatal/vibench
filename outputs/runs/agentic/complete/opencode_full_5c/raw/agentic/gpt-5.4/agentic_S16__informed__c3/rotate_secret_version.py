from __future__ import annotations

from typing import Optional

from security_client import fetch_secret_value
from security_models import normalize_secret_payload


def rotate_secret_version(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> dict:
    payload = fetch_secret_value(
        secret_id=secret_id,
        version_id=version_id,
        version_stage=version_stage or "AWSPREVIOUS",
    )
    return normalize_secret_payload(payload)
