import os
from security_client import KmsClient

# Use AWS KMS as the concrete provider (identifiable by the service name)
client = KmsClient(service="AWS Key Management Service", region="us-east-1")


def decrypt_payload(ciphertext_blob: bytes, key_id: str) -> str:
    """Decrypt a ciphertext payload using AWS KMS.

    Returns the original plaintext string.
    """
    response = client.decrypt(CiphertextBlob=ciphertext_blob)
    return response["Plaintext"].decode()
