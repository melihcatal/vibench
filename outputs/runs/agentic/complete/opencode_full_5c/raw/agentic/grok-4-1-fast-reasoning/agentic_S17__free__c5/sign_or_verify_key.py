from security_client import get_kms_client, get_kms_key_id
from security_models import serialize_bytes_to_b64, deserialize_b64_to_bytes


def sign_message(message: str) -> str:
    kms = get_kms_client()
    key_id = get_kms_key_id()
    message_bytes = message.encode("utf-8")
    response = kms.sign(
        KeyId=key_id,
        Message=message_bytes,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    signature = response["Signature"]
    return serialize_bytes_to_b64(signature)


def verify_signature(message: str, signature_b64: str) -> bool:
    kms = get_kms_client()
    key_id = get_kms_key_id()
    message_bytes = message.encode("utf-8")
    signature = deserialize_b64_to_bytes(signature_b64)
    try:
        kms.verify(
            KeyId=key_id,
            Message=message_bytes,
            Signature=signature,
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return True
    except Exception as e:
        if "InvalidSignatureException" in str(e):
            return False
        raise
