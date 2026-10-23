import os
from google.cloud import kms


def get_client():
    return kms.KeyManagementServiceClient()


def get_crypto_key_path(project_id, location_id, key_ring_id, key_id):
    client = get_client()
    return client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
