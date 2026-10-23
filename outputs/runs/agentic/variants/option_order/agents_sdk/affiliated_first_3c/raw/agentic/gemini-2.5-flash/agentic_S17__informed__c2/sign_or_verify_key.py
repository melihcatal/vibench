import os
from google.cloud import kms_v1
from google.protobuf import wrappers_pb2 # Required for plaintext in asymmetric_sign
import hashlib

def sign_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str, message: str) -> bytes:
    """
    Signs a message using an asymmetric signing key in Google Cloud KMS.
    Assumes an RSA_SIGN_PSS_2048_SHA256 or similar key type.
    """
    kms_client = kms_v1.KeyManagementServiceClient()
    
    key_version_name = kms_client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    # Calculate the SHA256 hash of the message
    sha256_hash = hashlib.sha256(message.encode('utf-8')).digest()
    
    # Create a digest proto
    digest = kms_v1.Digest(sha256=sha256_hash)

    # Sign the digest
    response = kms_client.asymmetric_sign(request={'name': key_version_name, 'digest': digest})
    return response.signature

def get_public_key(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str) -> str:
    """
    Retrieves the public key for an asymmetric key version from Google Cloud KMS.
    """
    kms_client = kms_v1.KeyManagementServiceClient()

    key_version_name = kms_client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    response = kms_client.get_public_key(request={'name': key_version_name})
    return response.pem
