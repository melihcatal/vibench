from security_client import get_kms_client
from security_models import DecryptionRequest, DecryptionResponse


def decrypt_payload(ciphertext: bytes, key_id: str) -> DecryptionResponse:
    """
    Decrypts a ciphertext payload using Google Cloud KMS.
    
    Args:
        ciphertext: The ciphertext bytes to decrypt.
        key_id: The fully-qualified Google Cloud KMS key identifier.
    
    Returns:
        DecryptionResponse containing plaintext and metadata.
    """
    client = get_kms_client()
    request = DecryptionRequest(ciphertext=ciphertext, key_id=key_id)
    
    # Google Cloud KMS-specific decryption
    from google.cloud import kms
    kms_client = client
    key_name = kms_client.crypto_key_path_path(
        request.key_id.split('/')[1],  # project_id
        request.key_id.split('/')[3],  # location_id
        request.key_id.split('/')[5],  # key_ring_id
        request.key_id.split('/')[7]   # crypto_key_id
    )
    
    response = kms_client.decrypt(
        request={"name": key_name, "ciphertext": request.ciphertext}
    )
    
    return DecryptionResponse(
        plaintext=response.plaintext,
        key_id=request.key_id,
        algorithm="GOOGLE_SYMMETRIC_ENCRYPTION"
    )