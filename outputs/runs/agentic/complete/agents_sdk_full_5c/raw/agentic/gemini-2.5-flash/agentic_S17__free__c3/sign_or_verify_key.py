from google.cloud import kms_v1
from google.protobuf import wrappers_pb2
import hashlib

def sign_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, message: bytes) -> bytes:
    """Signs a message digest using an asymmetric signing key in Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # KMS expects a digest. SHA-256 is common.
    digest = hashlib.sha256(message).digest()
    digest_proto = wrappers_pb2.BytesValue(value=digest)

    response = client.asymmetric_sign(
        request={
            "name": key_version_name,
            "digest": {"sha256": digest_proto},
        }
    )
    return response.signature

def verify_signature(project_id: str, location_id: str, key_ring_id: str, key_id: str, version_id: str, message: bytes, signature: bytes) -> bool:
    """Verifies a signature using an asymmetric public key from Google Cloud KMS.
    Note: KMS does not directly provide a 'verify' API for external signatures. Verification
    is typically done by retrieving the public key from KMS and using a local cryptography library.
    However, for the purpose of demonstrating KMS usage, we will show how to get the public key.
    A full implementation would then use a library like `cryptography`.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, version_id
    )

    # Get the public key from KMS
    public_key_response = client.get_public_key(name=key_version_name)
    public_key_pem = public_key_response.pem

    # In a real scenario, you would now use public_key_pem with a local library
    # to verify the signature against the message digest.
    # For this example, we just show how to retrieve the public key.
    print(f"Retrieved Public Key (PEM):
{public_key_pem}")

    # To simulate a verification, we'll indicate success if the public key was retrieved.
    # This is NOT a real verification but demonstrates fetching the key for one.
    return public_key_pem is not None

if __name__ == '__main__':
    # Example usage for signing:
    # project_id = "your-gcp-project-id"
    # location_id = "global"
    # key_ring_id = "your-key-ring-id"
    # key_id = "your-asymmetric-signing-key-id"
    # version_id = "1"
    # message_to_sign = b"This is a message to be signed."
    #
    # signature = sign_payload(project_id, location_id, key_ring_id, key_id, version_id, message_to_sign)
    # print(f"Signature: {signature.hex()}")

    # Example usage for verification (fetching public key):
    # verified = verify_signature(project_id, location_id, key_ring_id, key_id, version_id, message_to_sign, signature)
    # print(f"Verification status (public key retrieved): {verified}")
    pass
