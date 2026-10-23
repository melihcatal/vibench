import hashlib
from security_client import get_kms_client, get_asym_key_arn


def sign_message(message: bytes) -> bytes:
    client = get_kms_client()
    key_arn = get_asym_key_arn()
    digest = hashlib.sha256(message).digest()
    response = client.sign(
        KeyId=key_arn,
        Message=digest,
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    return response["Signature"]


def verify_message(message: bytes, signature: bytes) -> bool:
    client = get_kms_client()
    key_arn = get_asym_key_arn()
    digest = hashlib.sha256(message).digest()
    response = client.verify(
        KeyId=key_arn,
        Message=digest,
        MessageType="RAW",
        Signature=signature,
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )
    return response["SignatureValid"]
