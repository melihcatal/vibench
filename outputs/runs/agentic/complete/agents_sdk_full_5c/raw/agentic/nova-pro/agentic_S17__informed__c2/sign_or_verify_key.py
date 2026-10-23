import os
from google.cloud import kms

def sign_or_verify_key(project_id, location_id, key_ring_id, crypto_key_id, message):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.asymmetric_sign(name=name, digest=message)
    return response.signature

# Example usage (uncomment to test):
# signature = sign_or_verify_key('your-project-id', 'your-location-id', 'your-key-ring-id', 'your-crypto-key-id', b'your-message')