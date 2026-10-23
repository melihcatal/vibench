from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse
import os


def envelope_encrypt(plaintext: bytes, key_id: str) -> EnvelopeEncryptionResponse:
    """
    Implements envelope encryption using Google Cloud KMS for key encryption.
    
    Args:
        plaintext: The plaintext bytes to encrypt.
        key_id: The fully-qualified Google Cloud KMS key identifier.
    
    Returns:
        EnvelopeEncryptionResponse containing ciphertext, encrypted DEK, and metadata.
    """
    client = get_kms_client()
    request = EnvelopeEncryptionRequest(plaintext=plaintext, key_id=key_id)
    
    # Generate a data encryption key (DEK)
    dek = os.urandom(32)
    
    # Encrypt the DEK with Google Cloud KMS
    from google.cloud import kms
    kms_client = client
    key_name = kms_client.crypto_key_path_path(
        request.key_id.split('/')[1],  # project_id
        request.key_id.split('/')[3],  # location_id
        request.key_id.split('/')[5],  # key_ring_id
        request.key_id.split('/')[7]   # crypto_key_id
    )
    
    response = kms_client.encrypt(
        request={"name": key_name, "plaintext": dek}
    )
    encrypted_dek = response.ciphertext
    
    # Encrypt the plaintext with the DEK (AES-GCM)
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, request.plaintext, None)
    
    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek,
        nonce=nonce,
        key_id=request.key_id,
        algorithm="AES_256_GCM"
    )