from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext: bytes) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using AWS KMS.
    
    Args:
        ciphertext: The ciphertext bytes to decrypt.
    
    Returns:
        DecryptionResponse containing plaintext and metadata.
    """
    client = get_kms_client()
    response = client.decrypt(
        CiphertextBlob=ciphertext
    )
    
    return DecryptionResponse(
        plaintext=response["Plaintext"],
        key_id=response["KeyId"],
        algorithm=response.get("EncryptionAlgorithm", "SYMMETRIC_DEFAULT"),
        provider="aws_kms"
    )