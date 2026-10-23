from security_client import get_kms_client
from security_models import normalize_payload


def sign_message(key_id: str, message: Union[str, bytes]) -> bytes:
    kms = get_kms_client()
    msg = normalize_payload(message)
    response = kms.sign(
        KeyId=key_id, Message=msg, SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256"
    )
    return response["Signature"]


def verify_signature(key_id: str, message: Union[str, bytes], signature: bytes) -> bool:
    kms = get_kms_client()
    msg = normalize_payload(message)
    try:
        kms.verify(
            KeyId=key_id,
            Message=msg,
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return True
    except kms.exceptions.InvalidSignatureException:
        return False
