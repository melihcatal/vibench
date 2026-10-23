from __future__ import annotations

from security_client import kms_client
from security_models import SignatureResponse, VerificationResponse, b64encode_str


DEFAULT_SIGNING_ALGORITHM = "RSASSA_PSS_SHA_256"



def sign_with_kms(message: str, key_id: str, signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM) -> SignatureResponse:
    client = kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=message.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm=signing_algorithm,
    )
    return SignatureResponse(
        key_id=key_id,
        message_type="RAW",
        signing_algorithm=signing_algorithm,
        signature_b64=b64encode_str(response["Signature"]),
    )



def verify_with_kms(message: str, key_id: str, signature: bytes, signing_algorithm: str = DEFAULT_SIGNING_ALGORITHM) -> VerificationResponse:
    client = kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=message.encode("utf-8"),
        MessageType="RAW",
        Signature=signature,
        SigningAlgorithm=signing_algorithm,
    )
    return VerificationResponse(
        key_id=key_id,
        signature_valid=bool(response["SignatureValid"]),
        signing_algorithm=signing_algorithm,
    )
