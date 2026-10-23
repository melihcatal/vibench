from google.cloud import kms

def sign_or_verify_key(message, signature, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config['project_id'], config['location'], config['key_ring'], config['key_id'])
    response = client.asymmetric_decrypt(request={'name': name, 'ciphertext': signature})
    return response.plaintext == message