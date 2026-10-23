from google.cloud import kms
from google.protobuf import wrappers_pb2
from security_models import SignConfig
from security_client import get_kms_client

def sign_payload(payload_data: bytes, config: SignConfig):
    client = get_kms_client()
    name = client.crypto_key_version_path(
        config.project_id,
        config.location,
        config.key_ring,
        config.key_id,
        config.version
    )

    # Calculate the SHA256 hash of the data
    import hashlib
    digest = hashlib.sha256(payload_data).digest()

    # Create the AsymmetricSignRequest with the digest
    sign_request = {
        "name": name,
        "digest": {"sha256": digest},
        "digest_crc32c": wrappers_pb2.Int64Value(value=client.client_helper.crc32c(digest))
    }
    
    sign_response = client.asymmetric_sign(request=sign_request)
    return sign_response.signature

def verify_signature(payload_data: bytes, signature: bytes, config: SignConfig):
    client = get_kms_client()
    public_key = client.get_public_key(name=client.crypto_key_version_path(
        config.project_id,
        config.location,
        config.key_ring,
        config.key_id,
        config.version
    ))

    # In a real application, you would use a crypto library to verify the signature
    # against the public key and the digest of the payload_data.
    # For this example, we'll just indicate that a public key was retrieved.
    return True # Placeholder for actual verification logic
