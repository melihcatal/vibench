import os
from google.cloud import kms_v1
from google.protobuf import wrappers_pb2 # Required for passing data as bytes
from security_client import KmsClient

def sign_payload(payload: bytes, key_id: str, key_version: str) -> bytes:
    kms_client = KmsClient()
    name = kms_client.client.crypto_key_version_path(
        kms_client.project_id,
        kms_client.location_id,
        kms_client.key_ring_id,
        key_id,
        key_version,
    )

    # Create the digest. SHA256 is commonly used for signing.
    digest = wrappers_pb2.BytesValue(value=payload) # Assuming payload is already hashed or small enough

    response = kms_client.client.asymmetric_sign(name=name, digest=digest)
    return response.signature

def verify_signature(payload: bytes, signature: bytes, key_id: str, key_version: str) -> bool:
    kms_client = KmsClient()
    name = kms_client.client.crypto_key_version_path(
        kms_client.project_id,
        kms_client.location_id,
        kms_client.key_ring_id,
        key_id,
        key_version,
    )
    
    # Get the public key to verify the signature locally
    get_public_key_response = kms_client.client.get_public_key(name=name)
    public_key_pem = get_public_key_response.pem.encode("utf-8")

    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature

    public_key = serialization.load_pem_public_key(public_key_pem)

    try:
        public_key.verify(
            signature,
            payload,
            padding.PKCS1v15(),  # Or other padding schemes based on key config
            hashes.SHA256() # Or other hash algorithms based on key config
        )
        return True
    except InvalidSignature:
        return False
