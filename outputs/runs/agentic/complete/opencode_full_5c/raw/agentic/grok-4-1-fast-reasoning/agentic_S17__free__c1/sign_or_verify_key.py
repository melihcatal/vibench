import os
from security_client import get_kms_client


def sign_message(
    message: bytes,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> bytes:
    client = get_kms_client()
    key_id = key_id or os.getenv(
        "AWS_ASYMMETRIC_KMS_KEY_ID", os.getenv("AWS_KMS_KEY_ID")
    )
    if not key_id:
        raise ValueError("AWS_ASYMMETRIC_KMS_KEY_ID or AWS_KMS_KEY_ID required")
    response = client.sign(
        KeyId=key_id, Message=message, SigningAlgorithm=signing_algorithm
    )
    return response["Signature"]


def verify_signature(
    message: bytes,
    signature: bytes,
    key_id: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> bool:
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=message,
        Signature=signature,
        SigningAlgorithm=signing_algorithm,
    )
    return response["SignatureValid"]
