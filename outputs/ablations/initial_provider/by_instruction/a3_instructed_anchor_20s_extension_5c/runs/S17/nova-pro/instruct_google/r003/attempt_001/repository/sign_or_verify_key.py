from google.cloud import kms

def sign_or_verify_key(project_id, location_id, key_ring_id, crypto_key_id, data):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.asymmetric_sign(request={"name": key_name, "digest": {"sha256": hashlib.sha256(data).digest()}}}
    return response.signature

def verify_signature(project_id, location_id, key_ring_id, crypto_key_id, data, signature):
    client = kms.KeyManagementServiceClient()
    key_name = client.crypto_key_path_path(project_id, location_id, key_ring_id, crypto_key_id)
    response = client.asymmetric_decrypt_signature(request={"name": key_name, "digest": {"sha256": hashlib.sha256(data).digest()}, "signature": signature})
    return response.verified