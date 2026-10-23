import os
from google.cloud import kms

def sign_or_verify_key(message):
    client = kms.KeyManagementServiceClient()
    location_id = 'global'
    key_ring_id = 'my-key-ring'
    key_id = 'my-key'
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.asymmetric_sign(key_name, message.encode('utf-8'))
    return response.signature