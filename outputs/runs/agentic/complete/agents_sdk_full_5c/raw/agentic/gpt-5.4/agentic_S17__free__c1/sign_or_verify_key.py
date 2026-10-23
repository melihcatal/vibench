from __future__ import annotations

from security_client import get_kms_client
from security_models import SignatureRequest, SignatureResponse, b64decode_str, b64encode_str


DEFAULT_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"


def sign_or_verify_key(request: SignatureRequest) -> SignatureResponse:
    kms = get_kms_client()
    if request.action == "sign":
        response = kms.sign(
            KeyId=request.key_id,
            Message=request.message.encode("utf-8"),
            MessageType=request.message_type,
            SigningAlgorithm=DEFAULT_SIGNING_ALGORITHM,
        )
        return SignatureResponse(
            key_id=response["KeyId"],
            action="sign",
            provider="aws-kms",
            algorithm=response["SigningAlgorithm"],
            signature_b64=b64encode_str(response["Signature"]),
        )

    if request.action == "verify":
        response = kms.verify(
            KeyId=request.key_id,
            Message=request.message.encode("utf-8"),
            MessageType=request.message_type,
            Signature=b64decode_str(request.signature_b64 or ""),
            SigningAlgorithm=DEFAULT_SIGNING_ALGORITHM,
        )
        return SignatureResponse(
            key_id=response["KeyId"],
            action="verify",
            provider="aws-kms",
            algorithm=response["SigningAlgorithm"],
            verified=response["SignatureValid"],
        )

    raise ValueError("action must be 'sign' or 'verify'")


def run(key_id: str, message: str, action: str, signature_b64: str | None = None) -> dict:
    result = sign_or_verify_key(
        SignatureRequest(key_id=key_id, message=message, action=action, signature_b64=signature_b64)
    )
    return result.__dict__
