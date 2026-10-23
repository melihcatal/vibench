from __future__ import annotations

from security_client import kms_client, normalize_kms_key_id
from security_models import (
    SignVerifyRequest,
    SignVerifyResponse,
    b64decode_bytes,
    b64encode_text,
)


def sign_or_verify_key(request: SignVerifyRequest) -> SignVerifyResponse:
    client = kms_client()
    message = request.message.encode("utf-8")
    if request.action == "sign":
        response = client.sign(
            KeyId=normalize_kms_key_id(request.key_id),
            Message=message,
            MessageType="RAW",
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignVerifyResponse(
            key_id=response["KeyId"],
            action="sign",
            signature_b64=b64encode_text(response["Signature"]),
            valid=None,
        )
    response = client.verify(
        KeyId=normalize_kms_key_id(request.key_id),
        Message=message,
        MessageType="RAW",
        Signature=b64decode_bytes(request.signature_b64 or ""),
        SigningAlgorithm=request.signing_algorithm,
    )
    return SignVerifyResponse(
        key_id=response["KeyId"],
        action="verify",
        signature_b64=request.signature_b64,
        valid=bool(response["SignatureValid"]),
    )
