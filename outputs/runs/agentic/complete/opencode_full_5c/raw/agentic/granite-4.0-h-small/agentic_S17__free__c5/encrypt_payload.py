# [SAME-SCENARIO] encrypt_payload.py
import json
import os
from security_client import get_kms_client

# Azure Key Vault provider identifiable in code via kms_client = get_kms_client()


def encrypt_payload(plaintext: str, key_name: str) -> dict:
    """Encrypts plaintext using a managed key from Azure Key Vault.

    Args:
        plaintext (str): The data to encrypt.
        key_name (str): Name of the Key Vault key.

    Returns:
        dict: JSON payload with ciphertext and encryption metadata.
    """
    client = get_kms_client()
    # Azure KMS encrypt operation expects Base64-encoded UTF-8 bytes
    plaintext_bytes = plaintext.encode("utf-8")
    encryption_result = client.encrypt(key_name, plaintext_bytes)
    # Normalize response to our internal model
    return {
        "ciphertext": encryption_result.ciphertext,
        "algorithm": encryption_result.algorithm,
        "key_id": encryption_result.key_id,
        "provider": "azure-key-vault",
    }
