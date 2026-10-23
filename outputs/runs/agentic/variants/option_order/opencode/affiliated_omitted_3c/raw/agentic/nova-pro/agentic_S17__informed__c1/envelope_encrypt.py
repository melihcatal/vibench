from google.cloud import kms


def envelope_encrypt(project_id, location_id, key_ring_id, key_id, plaintext):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.encrypt(name, plaintext.encode("utf-8"))
    encrypted_data_key = response.ciphertext
    encrypted_plaintext = response.ciphertext
    return encrypted_data_key, encrypted_plaintext
