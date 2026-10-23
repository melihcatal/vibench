import base64
from security_client import get_kms_client, AWS_KMS_KEY_ID


def encrypt_payload(plaintext: str) -> str:
    kms_client = get_kms_client()
    if not AWS_KMS_KEY_ID:
        raise ValueError("AWS_KMS_KEY_ID environment variable not set.")

    response = kms_client.encrypt(
        KeyId=AWS_KMS_KEY_ID, Plaintext=plaintext.encode("utf-8")
    )

    ciphertext_blob = response["CiphertextBlob"]
    return base64.b64encode(ciphertext_blob).decode("utf-8")
