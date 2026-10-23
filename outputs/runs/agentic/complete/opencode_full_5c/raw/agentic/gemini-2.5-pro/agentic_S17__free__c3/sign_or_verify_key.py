import base64
from security_client import get_kms_client, AWS_KMS_KEY_ID


def sign_message(message: str) -> str:
    kms_client = get_kms_client()
    if not AWS_KMS_KEY_ID:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    response = kms_client.sign(
        KeyId=AWS_KMS_KEY_ID,
        Message=message.encode("utf-8"),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
    )

    signature = response["Signature"]
    return base64.b64encode(signature).decode("utf-8")


def verify_signature(message: str, signature_b64: str) -> bool:
    kms_client = get_kms_client()
    if not AWS_KMS_KEY_ID:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    try:
        signature = base64.b64decode(signature_b64)
        response = kms_client.verify(
            KeyId=AWS_KMS_KEY_ID,
            Message=message.encode("utf-8"),
            MessageType="RAW",
            Signature=signature,
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return response["SignatureValid"]
    except Exception:
        return False
