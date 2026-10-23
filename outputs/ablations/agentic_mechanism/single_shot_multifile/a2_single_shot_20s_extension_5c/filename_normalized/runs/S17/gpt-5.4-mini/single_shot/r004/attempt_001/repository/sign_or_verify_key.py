from __future__ import annotations

import os
from typing import Any, Dict

from security_client import get_security_client, get_kms_key_name
from security_models import SignatureRequest, SignatureResponse, VerificationRequest, VerificationResponse


def sign_or_verify_key(message: str, signature: str | None = None, key_name: str | None = None) -> SignatureResponse | VerificationResponse:
    client = get_security_client()
    resolved_key_name = get_kms_key_name(key_name)
    if signature:
        request = VerificationRequest(message=message, signature=signature, key_name=resolved_key_name)
        verification = client.verify(request=request)
        return VerificationResponse(
            key_name=resolved_key_name,
            valid=verification.valid,
            provider="google-cloud-kms",
            metadata=verification.metadata,
        )
    request = SignatureRequest(message=message, key_name=resolved_key_name)
    signing = client.sign(request=request)
    return SignatureResponse(
        key_name=resolved_key_name,
        signature=signing.signature,
        provider="google-cloud-kms",
        metadata=signing.metadata,
    )


def main() -> Dict[str, Any]:
    message = os.environ.get("MESSAGE", "")
    signature = os.environ.get("SIGNATURE")
    key_name = os.environ.get("KMS_KEY_NAME")
    response = sign_or_verify_key(message=message, signature=signature, key_name=key_name)
    return response.to_dict()
