from __future__ import annotations

from typing import Optional

from security_client import get_kms_client, get_kms_key_id
from security_models import SignatureResponse, VerificationResponse, b64decode_text, b64encode_bytes


AWS_KMS_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"


def sign_message(
    message: str,
    key_id: Optional[str] = None,
    signing_algorithm: str = AWS_KMS_SIGNING_ALGORITHM,
    message_type: str = "RAW",
) -> SignatureResponse:
    client = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    response = client.sign(
        KeyId=resolved_key_id,
        Message=message.encode("utf-8"),
        MessageType=message_type,
        SigningAlgorithm=signing_algorithm,
    )
    return SignatureResponse(
        key_id=response["KeyId"],
        signature_b64=b64encode_bytes(response["Signature"]),
        signing_algorithm=response["SigningAlgorithm"],
    )



def verify_message(
    message: str,
    signature_b64: str,
    key_id: Optional[str] = None,
    signing_algorithm: str = AWS_KMS_SIGNING_ALGORITHM,
    message_type: str = "RAW",
) -> VerificationResponse:
    client = get_kms_client()
    resolved_key_id = get_kms_key_id(key_id)
    response = client.verify(
        KeyId=resolved_key_id,
        Message=message.encode("utf-8"),
        MessageType=message_type,
        Signature=b64decode_text(signature_b64),
        SigningAlgorithm=signing_algorithm,
    )
    return VerificationResponse(
        key_id=response["KeyId"],
        signature_valid=response["SignatureValid"],
        signing_algorithm=response["SigningAlgorithm"],
    )
