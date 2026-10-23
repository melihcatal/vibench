from __future__ import annotations

from security_client import AWS_KMS_PROVIDER, AWS_KMS_SIGNING_ALGORITHM, get_kms_client
from security_models import (
    SignOrVerifyRequest,
    SignOrVerifyResponse,
    b64decode_str,
    b64encode_str,
)


def sign_or_verify_key(request: SignOrVerifyRequest) -> SignOrVerifyResponse:
    kms = get_kms_client()
    signing_algorithm = request.signing_algorithm or AWS_KMS_SIGNING_ALGORITHM
    message = request.message.encode("utf-8")
    if request.action == "sign":
        result = kms.sign(
            KeyId=request.key_id,
            Message=message,
            MessageType=request.message_type,
            SigningAlgorithm=signing_algorithm,
        )
        return SignOrVerifyResponse(
            provider=AWS_KMS_PROVIDER,
            key_id=result["KeyId"],
            action="sign",
            signature_b64=b64encode_str(result["Signature"]),
            signing_algorithm=result["SigningAlgorithm"],
        )
    if request.action == "verify":
        result = kms.verify(
            KeyId=request.key_id,
            Message=message,
            MessageType=request.message_type,
            Signature=b64decode_str(request.signature_b64 or ""),
            SigningAlgorithm=signing_algorithm,
        )
        return SignOrVerifyResponse(
            provider=AWS_KMS_PROVIDER,
            key_id=result["KeyId"],
            action="verify",
            verified=result["SignatureValid"],
            signing_algorithm=result["SigningAlgorithm"],
        )
    raise ValueError("action must be 'sign' or 'verify'")
