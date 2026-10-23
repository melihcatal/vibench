import os

from security_client import aws_region, kms_client, kms_key_id
from security_models import b64d, b64e


def sign_message(message: bytes, key_id: str = "") -> str:
    client = kms_client()
    resolved_key_id = key_id or kms_key_id()
    response = client.sign(KeyId=resolved_key_id, Message=message, MessageType="RAW", SigningAlgorithm="RSASSA_PSS_SHA_256")
    return b64e(response["Signature"])


def verify_message(message: bytes, signature_b64: str, key_id: str = "") -> bool:
    client = kms_client()
    resolved_key_id = key_id or kms_key_id()
    response = client.verify(KeyId=resolved_key_id, Message=message, MessageType="RAW", Signature=b64d(signature_b64), SigningAlgorithm="RSASSA_PSS_SHA_256")
    return bool(response.get("SignatureValid"))
