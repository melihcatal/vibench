import os
from security_client import AWSKMSClient
from security_models import EncryptRequest, normalize_encrypt_response


def encrypt_payload(key_id: str, plaintext: str) -> dict:
    """
    Encrypts a plaintext payload using AWS KMS.

    Args:
        key_id: AWS KMS key ID or ARN.
        plaintext: Plaintext string to encrypt.

    Returns:
        Dictionary containing ciphertext and metadata.
    """
    client = AWSKMSClient()
    request = EncryptRequest(key_id=key_id, plaintext=plaintext.encode("utf-8"))

    response = client.encrypt(key_id=request.key_id, plaintext=request.plaintext)

    normalized_response = normalize_encrypt_response(response)
    return {
        "ciphertext": normalized_response.ciphertext.hex(),
        "key_id": normalized_response.key_id,
        "algorithm": normalized_response.algorithm,
    }
