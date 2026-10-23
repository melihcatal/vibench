from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
import base64

def sign_data_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, data: bytes) -> bytes:
    """Signs data with a KMS key.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location (e.g., "global", "us-central1").
        key_ring_id: The ID of your key ring.
        key_id: The ID of your signing key.
        version_id: The ID of the key version to use (e.g., "1").
        data: The data to be signed.

    Returns:
        The signature of the data.
    """
    client = KeyManagementServiceClient()
    key_path = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    key_version_path = client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, version_id)

    # Calculate the SHA256 hash of the data
    import hashlib
    digest = hashlib.sha256(data).digest()

    request = kms_v1.AsymmetricSignRequest(
        name=key_version_path,
        digest={'sha256': digest}
    )
    response = client.asymmetric_sign(request)
    return response.signature

def verify_data_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, data: bytes, signature: bytes) -> bool:
    """Verifies data with a KMS key.

    Note: Google Cloud KMS does not directly provide a "verify" API for asymmetric keys.
    Verification is typically done client-side using the public key obtained from KMS.
    This function demonstrates how to get the public key and perform client-side verification
    for a typical RSA PSS SHA256 signature.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location (e.g., "global", "us-central1").
        key_ring_id: The ID of your key ring.
        key_id: The ID of your signing key.
        version_id: The ID of the key version to use (e.g., "1").
        data: The original data.
        signature: The signature to verify.

    Returns:
        True if the signature is valid, False otherwise.
    """
    client = KeyManagementServiceClient()
    key_version_path = client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, version_id)

    # Get the public key
    response = client.get_public_key(name=key_version_path)
    public_key_pem = response.pem

    # Use a cryptography library to verify the signature
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding, utils
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend

    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
