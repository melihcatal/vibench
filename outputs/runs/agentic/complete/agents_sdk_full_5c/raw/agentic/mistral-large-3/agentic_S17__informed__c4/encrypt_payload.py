import os
from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: bytes, key_id: str) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using AWS KMS.
    """
    client = get_kms_client()
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    return EncryptionResponse(
        ciphertext=response['CiphertextBlob'],
        key_id=key_id,
        algorithm=response['EncryptionAlgorithm']
    )