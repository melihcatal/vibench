from __future__ import annotations

import os
from typing import Dict

from security_client import access_secret_text, stage_secret_version
from security_models import SecretRequest


def rotate_secret_version(secret_id: str | None = None, staged_payload: Dict[str, str] | None = None, version: str = "latest") -> str:
    request = SecretRequest(secret_id=secret_id or os.environ.get("ROTATION_SECRET_ID", "rotation-target"), version=version)
    if staged_payload is not None:
        staged = stage_secret_version(request.secret_id, staged_payload)
        return staged.value
    return access_secret_text(request.secret_id, version=request.version).value
