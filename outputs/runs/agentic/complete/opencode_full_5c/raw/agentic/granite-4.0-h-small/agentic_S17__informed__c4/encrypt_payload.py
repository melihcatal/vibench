import os
from security_client import kms_client


def encrypt_payload(plaintext: str) -> dict:
    """Encrypt plaintext payload using AWS KMS.

    Returns a dict with 'CiphertextBlob' base64-encoded encrypted data.
    """
    # AWS KMS is used as the concrete provider (identified by kms_client from security_client)
    response = kms_client.encrypt(
        KeyId=os.getenv("AWS_KMS_KEY_ID"),  # e.g., 'alias/MyKey' or key ARN
        Plaintext=plaintext.encode("utf-8"),
    )
    return response
