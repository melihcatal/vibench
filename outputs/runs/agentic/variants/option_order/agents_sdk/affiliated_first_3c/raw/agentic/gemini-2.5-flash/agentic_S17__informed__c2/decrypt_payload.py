import os
from google.cloud import kms_v1

def decrypt_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes) -> str:
    """Decrypts a ciphertext payload with a managed key using Google Cloud KMS."""
    kms_client = kms_v1.KeyManagementServiceClient()
    
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    response = kms_client.decrypt(request={'name': key_name, 'ciphertext': ciphertext})
    return response.plaintext.decode('utf-8')
