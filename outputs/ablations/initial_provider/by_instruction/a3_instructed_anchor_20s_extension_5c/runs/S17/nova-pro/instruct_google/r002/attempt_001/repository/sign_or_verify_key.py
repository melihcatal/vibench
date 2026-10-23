from google.cloud import kms

def sign_or_verify_key(project_id, location_id, key_ring_id, crypto_key_id, data):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.asymmetric_sign(name=key_name, digest=data)
    return response.signature
