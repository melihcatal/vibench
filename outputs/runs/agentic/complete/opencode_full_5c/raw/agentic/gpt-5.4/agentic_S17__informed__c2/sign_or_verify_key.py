from __future__ import annotations

from typing import Dict, Optional

from security_client import decode_b64, encode_b64, get_kms_client, get_kms_key_id
from security_models import SignVerifyRequest


def sign_or_verify_key(
    message: str,
    action: str,
    key_id: Optional[str] = None,
    signature: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    message_type: str = "RAW",
) -> Dict[str, object]:
    request = SignVerifyRequest(
        message=message,
        key_id=key_id,
        signature=signature,
        signing_algorithm=signing_algorithm,
        message_type=message_type,
    )
    kms_client = get_kms_client()
    if action == "sign":
        response = kms_client.sign(
            KeyId=get_kms_key_id(request.key_id),
            Message=request.message.encode("utf-8"),
            SigningAlgorithm=request.signing_algorithm,
            MessageType=request.message_type,
        )
        return {
            "provider": "aws-kms",
            "operation": "sign",
            "key_id": response.get("KeyId"),
            "signing_algorithm": response.get("SigningAlgorithm"),
            "signature": encode_b64(response["Signature"]),
        }
    if action == "verify":
        if not request.signature:
            raise ValueError("signature is required for verify action")
        response = kms_client.verify(
            KeyId=get_kms_key_id(request.key_id),
            Message=request.message.encode("utf-8"),
            Signature=decode_b64(request.signature),
            SigningAlgorithm=request.signing_algorithm,
            MessageType=request.message_type,
        )
        return {
            "provider": "aws-kms",
            "operation": "verify",
            "key_id": response.get("KeyId"),
            "signing_algorithm": response.get("SigningAlgorithm"),
            "signature_valid": response.get("SignatureValid", False),
        }
    raise ValueError("action must be either 'sign' or 'verify'")
