from google.cloud import kms_v1
from google.protobuf import wrappers_pb2

def sign_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, message_digest: bytes) -> bytes:
    """Signs a message digest using an asymmetric key in Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the asymmetric signing key.
        version_id: The version of the key to use for signing.
        message_digest: The SHA256 or SHA384 message digest to sign.

    Returns:
        The signature.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Determine the hash algorithm used for the digest
    if len(message_digest) == 32:  # SHA-256
        digest = kms_v1.Digest(sha256=message_digest)
    elif len(message_digest) == 48:  # SHA-384
        digest = kms_v1.Digest(sha384=message_digest)
    else:
        raise ValueError("message_digest must be a SHA-256 (32 bytes) or SHA-384 (48 bytes) digest.")

    request = kms_v1.AsymmetricSignRequest(name=key_version_name, digest=digest)
    response = client.asymmetric_sign(request=request)
    return response.signature

def verify_signature(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, message_digest: bytes, signature: bytes) -> bool:
    """Verifies a signature using an asymmetric public key in Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the asymmetric signing key.
        version_id: The version of the key that generated the signature.
        message_digest: The SHA256 or SHA384 message digest that was signed.
        signature: The signature to verify.

    Returns:
        True if the signature is valid, False otherwise.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # To verify, we need the public key. We can get it from the key version.
    public_key_response = client.get_public_key(request={"name": key_version_name})
    public_key_pem = public_key_response.pem

    # Use a local cryptographic library to verify the signature with the public key.
    # In a real application, you'd use a robust cryptographic library like cryptography.
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature

    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8')
    )

    # Determine the hash algorithm used for the digest
    if len(message_digest) == 32:  # SHA-256
        algorithm = hashes.SHA256()
    elif len(message_digest) == 48:  # SHA-384
        algorithm = hashes.SHA384()
    else:
        raise ValueError("message_digest must be a SHA-256 (32 bytes) or SHA-384 (48 bytes) digest.")

    try:
        public_key.verify(
            signature,
            message_digest,
            padding.PKCS1v15(),  # Assuming PKCS1v15 padding for RSA_SIGN_PKCS1_2048_SHA256, etc.
            algorithm
        )
        return True
    except InvalidSignature:
        return False
