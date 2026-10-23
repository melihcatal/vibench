from __future__ import annotations

from security_client import get_kms_client
from security_models import (
    SignatureRequest,
    SignatureResponse,
    b64decode_bytes,
    b64encode_str,
    normalize_text,
)


def sign_or_verify_key(request: SignatureRequest) -> SignatureResponse:
    kms = get_kms_client()
    message = normalize_text(request.message).encode("utf-8")
    if request.action == "sign":
        response = kms.sign(
            KeyId=request.key_id,
            Message=message,
            MessageType="RAW",
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignatureResponse(
            key_id=response["KeyId"],
            provider="aws-kms",
            action="sign",
            signature=b64encode_str(response["Signature"]),
        )
    response = kms.verify(
        KeyId=request.key_id,
        Message=message,
        MessageType="RAW",
        SigningAlgorithm=request.signing_algorithm,
        Signature=b64decode_bytes(request.signature or ""),
    )
    return SignatureResponse(
        key_id=request.key_id,
        provider="aws-kms",
        action="verify",
        verified=bool(response["SignatureValid"]),
    )
