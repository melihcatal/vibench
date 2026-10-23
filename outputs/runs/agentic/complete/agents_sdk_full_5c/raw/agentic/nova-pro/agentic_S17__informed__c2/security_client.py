import os
from google.cloud import kms

def get_kms_client():
    return kms.KeyManagementServiceClient()

def get_project_id():
    return os.getenv('GOOGLE_CLOUD_PROJECT')

def get_location_id():
    return 'global'

def get_key_ring_id():
    return 'your-key-ring-id'

def get_crypto_key_id():
    return 'your-crypto-key-id'