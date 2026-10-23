import os
from security_client import get_aws_kms_client

# Configure KMS client using AWS credentials
_kms_client = get_aws_kms_client()


def encrypt_payload(plaintext: bytes, key_id: str) -> dict:
    """Encrypts plaintext using AWS KMS. Returns ciphertext blob and other metadata."""
    response = _kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)
    # Extract ciphertext blob and additional information
    return {
        "CiphertextBlob": response["CiphertextBlob"],
        "KeyId": key_id,
        "EncryptionAlgorithm": response.get("EncryptionAlgorithm"),
    }


def decrypt_payload(ciphertext_blob: bytes, key_id: str) -> dict:
    """Decrypts ciphertext blob using AWS KMS. Returns plaintext and metadata."""
    response = _kms_client.decrypt(CiphertextBlob=ciphertext_blob)
    return {
        "Plaintext": response["Plaintext"],
        "KeyId": key_id,
        "EncryptionAlgorithm": response.get("EncryptionAlgorithm"),
    }
