from __future__ import annotations

import os

from security_client import decrypt_with_kms

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID", "alias/default")


def decrypt_payload(ciphertext: str, encryption_context: dict[str, str] | None = None) -> str:
    response = decrypt_with_kms(
        ciphertext=ciphertext,
        key_id=AWS_KMS_KEY_ID,
        encryption_context=encryption_context or {},
        region_name=AWS_REGION,
    )
    return response.plaintext or ""
