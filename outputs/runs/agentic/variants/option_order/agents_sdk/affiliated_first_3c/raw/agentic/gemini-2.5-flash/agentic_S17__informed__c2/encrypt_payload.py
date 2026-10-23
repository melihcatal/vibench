import os
from google.cloud import kms_v1

def encrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: str) -> bytes:
    """Encrypts a plaintext payload with a managed key using Google Cloud KMS."""
    kms_client = kms_v1.KeyManagementServiceClient()
    
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    
    # Convert the plaintext to bytes
    plaintext_bytes = plaintext.encode('utf-8')

    response = kms_client.encrypt(request={'name': key_name, 'plaintext': plaintext_bytes})
    return response.ciphertext
