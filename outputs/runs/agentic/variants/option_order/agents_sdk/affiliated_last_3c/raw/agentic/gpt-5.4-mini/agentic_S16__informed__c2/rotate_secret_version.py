from __future__ import annotations

import os

from security_client import fetch_secret_string
from security_models import SecretRequest, normalize_text

# AWS Secrets Manager integration
ROTATION_SECRET_ID = os.getenv("ROTATION_SECRET_ID", "prod/rotate/secret")
ROTATION_STAGE = os.getenv("ROTATION_STAGE", "AWSCURRENT")
ROTATION_VERSION = os.getenv("ROTATION_VERSION")


def main() -> dict:
    request = SecretRequest(secret_id=ROTATION_SECRET_ID, version=ROTATION_VERSION, stage=ROTATION_STAGE)
    response = fetch_secret_string(request.secret_id, version=request.version, stage=request.stage)
    normalized = normalize_text(response.value)
    return {"secret_id": response.secret_id, "version": response.version, "stage": request.stage, "value": normalized.compact}
