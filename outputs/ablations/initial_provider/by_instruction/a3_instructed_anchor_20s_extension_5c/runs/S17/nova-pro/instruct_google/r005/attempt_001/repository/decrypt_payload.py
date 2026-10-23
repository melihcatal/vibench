from google.cloud import kms

def decrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, ciphertext):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.decrypt(name=key_name, ciphertext=ciphertext)
    return response.plaintext