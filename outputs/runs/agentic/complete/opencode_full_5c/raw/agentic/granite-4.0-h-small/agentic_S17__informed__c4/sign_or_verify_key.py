import os
from security_client import kms_client


def sign_payload(payload: str) -> dict:
    """Sign a payload using AWS KMS (supports RSA/ECDSA key types)."""
    # AWS KMS is used as the concrete provider (identified by kms_client from security_client)
    response = kms_client.sign(
        KeyId=os.getenv("AWS_KMS_KEY_ID"),
        Message=payload.encode("utf-8"),
        MessageType="RAW",
    )
    return {"Signature": response["Signature"], "KeyId": os.getenv("AWS_KMS_KEY_ID")}


def verify_signature(key_id: str, payload: str, signature: bytes) -> bool:
    """Verify a signature produced by sign_payload."""
    response = kms_client.verify(
        KeyId=key_id,
        Message=payload.encode("utf-8"),
        Signature=signature,
        MessageType="RAW",
    )
    return response["SignatureValid"]
