import os
from google.cloud import kms

def encrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, plaintext):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.encrypt(name=name, plaintext=plaintext)
    return response.ciphertext

# Example usage (uncomment to test):
# ciphertext = encrypt_payload('your-project-id', 'your-location-id', 'your-key-ring-id', 'your-crypto-key-id', b'your-plaintext')