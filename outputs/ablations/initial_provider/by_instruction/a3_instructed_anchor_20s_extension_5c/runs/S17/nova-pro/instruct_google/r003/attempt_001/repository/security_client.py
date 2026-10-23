import os
from google.cloud import kms

def get_client():
    return kms.KeyManagementServiceClient()

def get_key_name(project_id, location_id, key_ring_id, crypto_key_id):
    client = get_client()
    return client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)