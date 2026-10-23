from __future__ import annotations

from typing import Optional

from security_client import fetch_secret_payload


def read_secret_version(secret_id: str, *, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> dict:
    payload = fetch_secret_payload(secret_id, version_id=version_id, version_stage=version_stage or "AWSCURRENT")
    return {
        "provider": "aws-secrets-manager",
        "secret_id": payload.secret_id,
        "version_id": payload.version_id,
        "version_stages": list(payload.version_stages),
        "value": payload.value,
    }
