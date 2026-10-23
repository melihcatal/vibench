from google.cloud import kms


def encrypt_payload(project_id, location_id, key_ring_id, key_id, plaintext):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.encrypt(name=name, plaintext=plaintext)
    return response.ciphertext
