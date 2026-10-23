import base64
import os
from google.cloud import kms_v1

def get_project_id() -> str:
    return os.getenv('GOOGLE_CLOUD_PROJECT', '')

def get_location() -> str:
    return os.getenv('KMS_LOCATION', 'global')

def get_key_ring() -> str:
    return os.getenv('KMS_KEY_RING', 'default-ring')

def get_key_name(key_name: str | None = None) -> str:
    if key_name:
        return key_name
    project = get_project_id()
    location = get_location()
    ring = get_key_ring()
    key = os.getenv('KMS_KEY_NAME', 'default-key')
    return f'projects/{project}/locations/{location}/keyRings/{ring}/cryptoKeys/{key}'

def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    return kms_v1.KeyManagementServiceClient()

def get_kms_key_name(key_name: str | None = None) -> str:
    return get_key_name(key_name)

def encode_bytes(value: str) -> bytes:
    try:
        return base64.b64decode(value)
    except Exception:
        return value.encode('utf-8')

def decode_bytes(value: bytes) -> str:
    return base64.b64encode(value).decode('utf-8')
