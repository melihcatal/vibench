from google.cloud import kms

def encrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.encrypt(name=key_name, plaintext=plaintext)
    return response.ciphertext
