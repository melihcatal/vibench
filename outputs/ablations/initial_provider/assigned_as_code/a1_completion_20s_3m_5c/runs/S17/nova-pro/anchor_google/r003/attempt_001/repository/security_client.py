from google.cloud import kms

def get_kms_client(config=None):
    config = config or {}
    return kms.KeyManagementServiceClient()

def get_key_id(config=None):
    config = config or {}
    return client.crypto_key_path(config['project_id'], config['location'], config['key_ring'], config['key_id'])