# [SAME-SCENARIO] decrypt_payload.py
import json
import os
from security_client import get_kms_client

# Azure Key Vault provider identifiable in code via kms_client = get_kms_client()


def decrypt_payload(ciphertext_payload: dict) -> str:
    """Decrypts a ciphertext payload using a managed key from Azure Key Vault.

    Args:
        ciphertext_payload (dict): Payload containing ciphertext and encryption metadata.

    Returns:
        str: Decrypted plaintext string.
    """
    client = get_kms_client()
    # Pass the raw ciphertext (bytes) and required metadata to the KMS client
    plaintext_bytes = client.decrypt(
        ciphertext_payload["ciphertext"],
        algorithm=ciphertext_payload.get("algorithm"),
        key_id=ciphertext_payload.get("key_id"),
    )
    return plaintext_bytes.decode("utf-8")
