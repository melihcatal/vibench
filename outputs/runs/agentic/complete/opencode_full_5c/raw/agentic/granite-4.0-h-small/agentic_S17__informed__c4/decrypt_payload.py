import os
from security_client import kms_client


def decrypt_payload(ciphertext_blob: bytes) -> str:
    """Decrypt ciphertext payload using AWS KMS.

    Expects the base64-encoded ciphertext blob (as returned by encrypt_payload).
    """
    # AWS KMS is used as the concrete provider (identified by kms_client from security_client)
    response = kms_client.decrypt(CiphertextBlob=ciphertext_blob)
    return response["Plaintext"].decode("utf-8")
