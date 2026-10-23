from google.cloud import kms

def envelope_encrypt(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.encrypt(name=key_name, plaintext=plaintext)
    ciphertext = response.ciphertext
    # Generate a new data encryption key
    data_key = b'\x00' * 32  # Example key, should be securely generated
    data_ciphertext = client.encrypt(name=key_name, plaintext=data_key).ciphertext
    return data_ciphertext, ciphertext
