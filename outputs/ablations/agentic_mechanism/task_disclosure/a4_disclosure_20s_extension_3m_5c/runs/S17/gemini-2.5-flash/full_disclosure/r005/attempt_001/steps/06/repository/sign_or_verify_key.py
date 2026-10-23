import hashlib
from google.cloud import kms_v1

def sign_message(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, message_bytes: bytes) -> bytes:
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_path_version(project_id, location_id, key_ring_id, key_id, version_id)
    
    digest = hashlib.sha256(message_bytes).digest()
    
    sign_request = kms_v1.types.AsymmetricSignRequest(
        name=key_version_name,
        digest=kms_v1.types.Digest(sha256=digest),
    )
    
    response = client.asymmetric_sign(request=sign_request)
    return response.signature

def get_public_key_for_verification(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str) -> str:
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_path_version(project_id, location_id, key_ring_id, key_id, version_id)
    
    response = client.get_public_key(name=key_version_name)
    return response.pem