from __future__ import annotations

import os

from security_client import encrypt_with_kms
from security_models import KeyRequest

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID", "alias/default")


def encrypt_payload(plaintext: str, encryption_context: dict[str, str] | None = None) -> str:
    request = KeyRequest(key_id=AWS_KMS_KEY_ID, plaintext=plaintext, encryption_context=encryption_context or {})
    response = encrypt_with_kms(request, region_name=AWS_REGION)
    return response.ciphertext or ""
