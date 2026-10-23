import boto3
from typing import str, bytes, bool


def sign_message(message: str, key_id: str) -> bytes:
    kms = boto3.client("kms")
    msg_bytes = message.encode("utf-8")
    response = kms.sign(
        KeyId=key_id, Message=msg_bytes, SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256"
    )
    return response["Signature"]


def verify_signature(message: str, signature: bytes, key_id: str) -> bool:
    kms = boto3.client("kms")
    msg_bytes = message.encode("utf-8")
    try:
        kms.verify(
            KeyId=key_id,
            Message=msg_bytes,
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return True
    except Exception:
        return False
