from __future__ import annotations

import base64
import hashlib

from security_client import AWS_KMS_PROVIDER, get_kms_client
from security_models import SigningRequest, SigningResponse


def sign_or_verify_key(
    request: SigningRequest, region_name: str | None = None
) -> SigningResponse:
    kms = get_kms_client(region_name)
    digest = hashlib.sha256(request.message_bytes()).digest()
    if request.signature_b64:
        verified = kms.verify(
            KeyId=request.key_name,
            Message=digest,
            MessageType="DIGEST",
            Signature=base64.b64decode(request.signature_b64.encode("utf-8")),
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return SigningResponse(
            key_name=request.key_name,
            provider=AWS_KMS_PROVIDER,
            verified=verified["SignatureValid"],
        )
    signed = kms.sign(
        KeyId=request.key_name,
        Message=digest,
        MessageType="DIGEST",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return SigningResponse(
        key_name=request.key_name,
        provider=AWS_KMS_PROVIDER,
        signature_b64=base64.b64encode(signed["Signature"]).decode("utf-8"),
    )
