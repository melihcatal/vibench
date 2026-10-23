import json
from security_client import KeyManagementClient


def encrypt_payload(plaintext: str, key_name: str) -> dict:
    """Encrypt a plaintext payload using a managed key.

    Uses the configured KMS client to invoke envelope encryption.
    Returns a dict containing ciphertext, encryption context, and other metadata.
    """
    client = KeyManagementClient()
    response = client.encrypt(key_name, plaintext)
    # response is assumed to be a dict with fields defined by the provider
    return response
