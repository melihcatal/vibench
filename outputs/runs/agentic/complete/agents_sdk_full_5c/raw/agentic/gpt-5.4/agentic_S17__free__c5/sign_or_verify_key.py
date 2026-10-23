from __future__ import annotations

from typing import Optional

from security_client import DEFAULT_KMS_SIGNING_ALGORITHM, get_kms_client
from security_models import SignVerifyRequest, SignVerifyResponse, b64decode_str, b64encode_str


def sign_or_verify_key(
    key_id: str,
    message: str,
    action: str = "sign",
    signature_b64: Optional[str] = None,
    signing_algorithm: str = DEFAULT_KMS_SIGNING_ALGORITHM,
    region_name: Optional[str] = None,
) -> SignVerifyResponse:
    request = SignVerifyRequest(
        key_id=key_id,
        message=message,
        action=action,
        signature_b64=signature_b64,
        signing_algorithm=signing_algorithm,
    )
    kms = get_kms_client(region_name)
    message_bytes = request.message.encode("utf-8")
    if request.action == "sign":
        response = kms.sign(
            KeyId=request.key_id,
            Message=message_bytes,
            MessageType=request.message_type,
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignVerifyResponse(
            action="sign",
            key_id=response["KeyId"],
            signature_b64=b64encode_str(response["Signature"]),
            signing_algorithm=response["SigningAlgorithm"],
        )
    if request.action == "verify":
        if not request.signature_b64:
            raise ValueError("signature_b64 is required for verify action")
        response = kms.verify(
            KeyId=request.key_id,
            Message=message_bytes,
            MessageType=request.message_type,
            Signature=b64decode_str(request.signature_b64),
            SigningAlgorithm=request.signing_algorithm,
        )
        return SignVerifyResponse(
            action="verify",
            key_id=response["KeyId"],
            verified=response["SignatureValid"],
            signing_algorithm=response["SigningAlgorithm"],
        )
    raise ValueError("action must be 'sign' or 'verify'")
