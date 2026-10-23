from __future__ import annotations

from typing import Literal, Optional
import hashlib

from security_client import get_kms_client
from security_models import SignatureResponse, b64decode_text, b64encode_bytes, normalize_text_payload


KmsAction = Literal["sign", "verify"]



def sign_or_verify_key(
    key_id: str,
    message: str,
    action: KmsAction = "sign",
    signature_b64: Optional[str] = None,
    signing_algorithm: str = "RSASSA_PSS_SHA_256",
    region_name: Optional[str] = None,
) -> SignatureResponse:
    kms = get_kms_client(region_name=region_name)
    digest = hashlib.sha256(normalize_text_payload(message).encode("utf-8")).digest()

    if action == "sign":
        response = kms.sign(
            KeyId=key_id,
            Message=digest,
            MessageType="DIGEST",
            SigningAlgorithm=signing_algorithm,
        )
        return SignatureResponse(
            key_id=key_id,
            action="sign",
            algorithm=response["SigningAlgorithm"],
            signature_b64=b64encode_bytes(response["Signature"]),
            metadata={"service": "AWS KMS", "sdk": "boto3"},
        )

    if not signature_b64:
        raise ValueError("signature_b64 is required for verify action")

    response = kms.verify(
        KeyId=key_id,
        Message=digest,
        MessageType="DIGEST",
        Signature=b64decode_text(signature_b64),
        SigningAlgorithm=signing_algorithm,
    )
    return SignatureResponse(
        key_id=key_id,
        action="verify",
        algorithm=response["SigningAlgorithm"],
        verified=response["SignatureValid"],
        metadata={"service": "AWS KMS", "sdk": "boto3"},
    )
