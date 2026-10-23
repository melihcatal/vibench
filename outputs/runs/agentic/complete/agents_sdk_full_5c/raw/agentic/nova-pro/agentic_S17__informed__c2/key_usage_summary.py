import os
from google.cloud import kms

def get_key_usage_summary(project_id, location_id, key_ring_id, crypto_key_id):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.get_crypto_key(name=name)
    return response.name, response.create_time

# Example usage (uncomment to test):
# key_name, create_time = get_key_usage_summary('your-project-id', 'your-location-id', 'your-key-ring-id', 'your-crypto-key-id')