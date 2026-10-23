from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: bytes, key_id: str) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using AWS KMS.
    
    Args:
        plaintext: The plaintext bytes to encrypt.
        key_id: The AWS KMS key ID or ARN.
    
    Returns:
        EncryptionResponse containing ciphertext and metadata.
    """
    client = get_kms_client()
    response = client.encrypt(
        KeyId=key_id,
        Plaintext=plaintext
    )
    
    return EncryptionResponse(
        ciphertext=response["CiphertextBlob"],
        key_id=key_id,
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        provider="aws_kms"
    )