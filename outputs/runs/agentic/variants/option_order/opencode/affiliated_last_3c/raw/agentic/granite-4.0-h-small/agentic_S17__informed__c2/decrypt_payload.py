import json
from security_client import KeyManagementClient


def decrypt_payload(ciphertext_blob: bytes, key_name: str) -> str:
    """Decrypt a ciphertext payload using a managed key.

    Uses the configured KMS client to invoke envelope decryption.
    Returns the original plaintext string.
    """
    client = KeyManagementClient()
    plaintext = client.decrypt(key_name, ciphertext_blob)
    return plaintext
