from __future__ import annotations

from typing import Optional

from security_client import get_kms_client, get_kms_key_id
from security_models import SignatureResponse, b64encode_bytes, b64decode_to_bytes

AWS_KMS_RSA_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"


def sign_message(message: str, key_id: Optional[str] = None) -> SignatureResponse:
    kms = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    response = kms.sign(
        KeyId=resolved_key_id,
        Message=message.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm=AWS_KMS_RSA_SIGNING_ALGORITHM,
    )
    return SignatureResponse(
        key_id=response["KeyId"],
        message_type=response["MessageType"],
        signing_algorithm=response["SigningAlgorithm"],
        signature_b64=b64encode_bytes(response["Signature"]),
    )


def verify_message(message: str, signature_b64: str, key_id: Optional[str] = None) -> SignatureResponse:
    kms = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    response = kms.verify(
        KeyId=resolved_key_id,
        Message=message.encode("utf-8"),
        MessageType="RAW",
        Signature=b64decode_to_bytes(signature_b64),
        SigningAlgorithm=AWS_KMS_RSA_SIGNING_ALGORITHM,
    )
    return SignatureResponse(
        key_id=response["KeyId"],
        message_type=response["MessageType"],
        signing_algorithm=response["SigningAlgorithm"],
        signature_b64=signature_b64,
        verified=response["SignatureValid"],
    )
