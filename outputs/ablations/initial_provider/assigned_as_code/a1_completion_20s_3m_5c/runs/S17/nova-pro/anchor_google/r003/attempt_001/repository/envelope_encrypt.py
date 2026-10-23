from google.cloud import kms

def envelope_encrypt(plaintext, config=None):
    config = config or {}
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(config['project_id'], config['location'], config['key_ring'], config['key_id'])
    data_key = client.generate_data_key(request={'name': name, 'key_spec': 'AES_256'})
    ciphertext_data_key = data_key.ciphertext
    plaintext_data_key = data_key.plaintext
    encrypted_data = client.encrypt(request={'name': name, 'plaintext': plaintext})
    ciphertext_blob = encrypted_data.ciphertext
    return ciphertext_blob, ciphertext_data_key