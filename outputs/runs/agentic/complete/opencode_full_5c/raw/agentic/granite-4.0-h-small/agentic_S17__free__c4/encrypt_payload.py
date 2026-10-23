import os, base64, json
from security_client import get_key_management_client

# AWS KMS integration – the client uses the AWS KMS service


def encrypt_payload(plaintext: str, key_id: str) -> str:
    """Encrypt a plaintext string using a managed KMS key.

    Returns the ciphertext as a base64‑encoded string.
    """
    client = get_key_management_client()
    # Call the managed service – AWS KMS encrypt API
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext.encode("utf-8"))
    # The ciphertext is returned as bytes; encode for transport
    ciphertext = response["CiphertextBlob"]
    return base64.b64encode(ciphertext).decode("utf-8")
