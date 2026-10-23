import os
from security_client import get_kms_client
from security_models import plaintext_to_bytes, encode_ciphertext, decode_ciphertext


def sign_message(
    message: str,
    key_id: str = None,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> str:
    key_id = key_id or os.getenv("KMS_KEY_ID")
    client = get_kms_client()
    response = client.sign(
        KeyId=key_id,
        Message=plaintext_to_bytes(message),
        MessageType="RAW",
        SigningAlgorithm=signing_algorithm,
    )
    return encode_ciphertext(response["Signature"])


def verify_signature(
    message: str,
    signature_b64: str,
    key_id: str,
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256",
) -> bool:
    client = get_kms_client()
    response = client.verify(
        KeyId=key_id,
        Message=plaintext_to_bytes(message),
        MessageType="RAW",
        Signature=decode_ciphertext(signature_b64),
        SigningAlgorithm=signing_algorithm,
    )
    return response["SignatureValid"]
