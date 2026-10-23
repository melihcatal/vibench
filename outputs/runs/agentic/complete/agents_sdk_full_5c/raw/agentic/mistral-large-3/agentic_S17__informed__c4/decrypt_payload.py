import os
from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext: bytes) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    """
    client = get_kms_client()
    response = client.decrypt(
        CiphertextBlob=ciphertext
    )
    return DecryptionResponse(
        plaintext=response['Plaintext'],
        key_id=response['KeyId'],
        algorithm=response['EncryptionAlgorithm']
    )