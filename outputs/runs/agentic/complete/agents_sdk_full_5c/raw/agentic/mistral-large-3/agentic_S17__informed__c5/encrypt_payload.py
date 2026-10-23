from security_client import get_kms_client
from security_models import EncryptionRequest, EncryptionResponse


def encrypt_payload(plaintext: bytes, key_id: str) -> EncryptionResponse:
    """
    Encrypts a plaintext payload using Google Cloud KMS.
    
    Args:
        plaintext: The plaintext bytes to encrypt.
        key_id: The fully-qualified Google Cloud KMS key identifier.
    
    Returns:
        EncryptionResponse containing ciphertext and metadata.
    """
    client = get_kms_client()
    request = EncryptionRequest(plaintext=plaintext, key_id=key_id)
    
    # Google Cloud KMS-specific encryption
    from google.cloud import kms
    kms_client = client
    key_name = kms_client.crypto_key_path_path(
        request.key_id.split('/')[1],  # project_id
        request.key_id.split('/')[3],  # location_id
        request.key_id.split('/')[5],  # key_ring_id
        request.key_id.split('/')[7]   # crypto_key_id
    )
    
    response = kms_client.encrypt(
        request={"name": key_name, "plaintext": request.plaintext}
    )
    
    return EncryptionResponse(
        ciphertext=response.ciphertext,
        key_id=request.key_id,
        algorithm="GOOGLE_SYMMETRIC_ENCRYPTION"
    )