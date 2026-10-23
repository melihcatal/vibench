from google.cloud import kms

def get_client(config=None):
    config = config or {}
    return kms.KeyManagementServiceClient()

def get_crypto_key_path(client, project_id, location, key_ring, key_id):
    return client.crypto_key_path(project_id, location, key_ring, key_id)