from google.cloud import kms


def sign_or_verify_key(project_id, location_id, key_ring_id, key_id, data):
    client = kms.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    response = client.asymmetric_sign(name=name, digest=data)
    return response.signature
