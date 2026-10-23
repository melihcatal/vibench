import os
from google.cloud import kms

def decrypt_payload(project_id, location_id, key_ring_id, crypto_key_id, ciphertext):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.decrypt(name=name, ciphertext=ciphertext)
    return response.plaintext

# Example usage (uncomment to test):
# plaintext = decrypt_payload('your-project-id', 'your-location-id', 'your-key-ring-id', 'your-crypto-key-id', b'your-ciphertext')