import hashlib
from security_client import get_kms_client
from security_models import encode_base64, decode_base64


def sign_payload(key_id: str, message: str) -> str:
    kms_client = get_kms_client()
    message_bytes = message.encode("utf-8")
    message_digest = hashlib.sha256(message_bytes).digest()

    response = kms_client.sign(
        KeyId=key_id,
        Message=message_digest,
        MessageType="DIGEST",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA256",
    )
    signature = response["Signature"]
    return encode_base64(signature)


def verify_signature(key_id: str, message: str, signature_b64: str) -> bool:
    kms_client = get_kms_client()
    message_bytes = message.encode("utf-8")
    message_digest = hashlib.sha256(message_bytes).digest()
    signature = decode_base64(signature_b64)

    response = kms_client.verify(
        KeyId=key_id,
        Message=message_digest,
        MessageType="DIGEST",
        Signature=signature,
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA256",
    )
    return response["SignatureValid"]
