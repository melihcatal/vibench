from __future__ import annotations

from typing import Any, Dict, Optional

from security_client import get_kms_client
from security_models import SignatureResponse, b64decode_str, b64encode_str, to_bytes


def sign_or_verify_key(
    action: str,
    key_id: str,
    message: str,
    signature_b64: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    region_name: Optional[str] = None,
) -> Dict[str, Any]:
    kms_client = get_kms_client(region_name)
    normalized_action = action.lower().strip()
    if normalized_action == "sign":
        response = kms_client.sign(
            KeyId=key_id,
            Message=to_bytes(message),
            MessageType="RAW",
            SigningAlgorithm=signing_algorithm,
        )
        return SignatureResponse(
            provider="aws-kms",
            key_id=response["KeyId"],
            algorithm=response["SigningAlgorithm"],
            action="sign",
            signature_b64=b64encode_str(response["Signature"]),
            message_type=response.get("MessageType", "RAW"),
        ).to_dict()
    if normalized_action == "verify":
        if not signature_b64:
            raise ValueError("signature_b64 is required for verify action")
        response = kms_client.verify(
            KeyId=key_id,
            Message=to_bytes(message),
            MessageType="RAW",
            Signature=b64decode_str(signature_b64),
            SigningAlgorithm=signing_algorithm,
        )
        return SignatureResponse(
            provider="aws-kms",
            key_id=key_id,
            algorithm=signing_algorithm,
            action="verify",
            verified=bool(response["SignatureValid"]),
            message_type=response.get("MessageType", "RAW"),
        ).to_dict()
    raise ValueError("action must be either 'sign' or 'verify'")
