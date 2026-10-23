import os
from google.cloud import kms

def encrypt_payload(plaintext):
    client = kms.KeyManagementServiceClient()
    location_id = 'global'
    key_ring_id = 'my-key-ring'
    key_id = 'my-key'
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.encrypt(key_name, plaintext.encode('utf-8'))
    return response.ciphertext