import os
from security_client import KmsClient

# Use AWS KMS as the concrete provider (identifiable by the service name)
client = KmsClient(service="AWS Key Management Service", region="us-east-1")


def encrypt_payload(plaintext: str, key_id: str) -> dict:
    """Encrypt a plaintext payload using AWS KMS.

    Returns a dict containing the ciphertext (Base64) and additional metadata.
    """
    response = client.encrypt(KeyId=key_id, Plaintext=plaintext.encode())
    return {
        "CiphertextBlob": response["CiphertextBlob"],
        "KeyId": key_id,
        "EncryptionAlgorithm": response.get("EncryptionAlgorithm"),
    }
