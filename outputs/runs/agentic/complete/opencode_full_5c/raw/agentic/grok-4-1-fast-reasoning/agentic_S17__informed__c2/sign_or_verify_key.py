import boto3
from security_client import get_kms_client
from typing import Optional


def sign_message(message: bytes, key_id: str, region: Optional[str] = None) -> bytes:
    client = get_kms_client(region)
    resp = client.sign(
        KeyId=key_id,
        Message=message,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    return resp["Signature"]


def verify_signature(
    message: bytes, signature: bytes, key_id: str, region: Optional[str] = None
) -> bool:
    client = get_kms_client(region)
    try:
        client.verify(
            KeyId=key_id,
            Message=message,
            MessageType="RAW",
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return True
    except client.exceptions.KMSInvalidSignatureException:
        return False
