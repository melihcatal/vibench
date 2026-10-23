from __future__ import annotations

from security_client import aws_kms_client, kms_key_id
from security_models import (
    SignVerifyRequest,
    SignVerifyResponse,
    b64decode_text,
    b64encode_bytes,
    normalize_plaintext,
    sha256_hex,
)


def sign_or_verify_key(request: SignVerifyRequest) -> SignVerifyResponse:
    client = aws_kms_client()
    key_id = kms_key_id(request.key_id)
    message = normalize_plaintext(request.message)
    if request.operation.lower() == "sign":
        response = client.sign(
            KeyId=key_id,
            Message=message,
            MessageType="RAW",
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignVerifyResponse(
            key_id=response["KeyId"],
            provider="aws-kms",
            signing_algorithm=response["SigningAlgorithm"],
            message_sha256=sha256_hex(message),
            signature=b64encode_bytes(response["Signature"]),
            valid=None,
        )
    if request.operation.lower() == "verify":
        if not request.signature:
            raise ValueError("signature is required for verify")
        response = client.verify(
            KeyId=key_id,
            Message=message,
            MessageType="RAW",
            Signature=b64decode_text(request.signature),
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignVerifyResponse(
            key_id=response["KeyId"],
            provider="aws-kms",
            signing_algorithm=response["SigningAlgorithm"],
            message_sha256=sha256_hex(message),
            signature=request.signature,
            valid=bool(response["SignatureValid"]),
        )
    raise ValueError("operation must be 'sign' or 'verify'")
