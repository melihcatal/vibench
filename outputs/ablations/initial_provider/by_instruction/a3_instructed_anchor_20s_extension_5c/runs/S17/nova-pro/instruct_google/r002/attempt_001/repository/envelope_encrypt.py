from google.cloud import kms

def envelope_encrypt(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.encrypt(name=key_name, plaintext=plaintext)
    ciphertext = response.ciphertext
    # Simulate envelope encryption by encrypting the ciphertext again
    response = client.encrypt(name=key_name, plaintext=ciphertext)
    return response.ciphertext
