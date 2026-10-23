from __future__ import annotations

import os

from security_client import sign_with_kms, verify_with_kms
from security_models import SigningRequest

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID", "alias/signing-key")


def sign_or_verify_key(message: bytes, signature: str | None = None) -> dict[str, str | bool | None]:
    request = SigningRequest(key_id=AWS_KMS_KEY_ID, message=message)
    if signature is None:
        result = sign_with_kms(request, region_name=AWS_REGION)
        return {"key_id": result.key_id, "signature": result.signature, "verified": result.verified}
    result = verify_with_kms(request, signature=signature, region_name=AWS_REGION)
    return {"key_id": result.key_id, "signature": result.signature, "verified": result.verified}
