from google.cloud import kms


def decrypt_payload(project_id, location_id, key_ring_id, key_id, ciphertext):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.decrypt(name=name, ciphertext=ciphertext)
    return response.plaintext
