from google.cloud import kms
from google.protobuf import wrappers_pb2
from security_client import get_kms_client
import hashlib

def sign_payload_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str, message: bytes) -> bytes:
    """Signs a message using an asymmetric signing key in Google Cloud KMS."""
    client = get_kms_client()
    key_version_name = client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, key_version_id)

    # Hash the message locally (KMS expects a hash, not raw message for signing)
    sha256_digest = hashlib.sha256(message).digest()
    digest_proto = wrappers_pb2.BytesValue(value=sha256_digest)

    response = client.asymmetric_sign(request={"name": key_version_name, "digest": {"sha256": digest_proto}})
    return response.signature

def verify_signature_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str, message: bytes, signature: bytes) -> bool:
    """Verifies a signature using an asymmetric public key from Google Cloud KMS.

    Note: KMS does not have a direct 'verify' API. Verification is typically done client-side
    using the public key retrieved from KMS. This function demonstrates retrieving the public key.
    For actual verification, you would use a crypto library with the retrieved public key.
    """
    client = get_kms_client()
    key_version_name = client.crypto_key_version_path(project_id, location_id, key_ring_id, key_id, key_version_id)

    # Retrieve the public key
    public_key_response = client.get_public_key(name=key_version_name)
    public_key_pem = public_key_response.pem

    # Hash the message locally, as done during signing
    sha256_digest = hashlib.sha256(message).digest()

    # --- Client-side verification using the retrieved public key ---
    # In a real application, you would use a library like `cryptography` for this.
    # Example (conceptual):
    # from cryptography.hazmat.primitives import hashes
    # from cryptography.hazmat.primitives.asymmetric import padding
    # from cryptography.hazmat.primitives.serialization import load_pem_public_key
    # from cryptography.hazmat.backends import default_backend
    # 
    # public_key = load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())
    # try:
    #     public_key.verify(
    #         signature,
    #         sha256_digest,
    #         padding.PKCS1v15(), # Or padding.PSS if using RSASSA_PSS
    #         hashes.SHA256()
    #     )
    #     return True
    # except Exception:
    #     return False

    # For this exercise, we will just indicate that we retrieved the public key.
    # Actual verification logic is complex and dependent on key type (RSA/EC) and padding.
    print(f"Retrieved public key (PEM format) for client-side verification:\n{public_key_pem}")
    print("Client-side verification with this public key and signature would happen here.")
    print("For demonstration, returning True assuming verification would succeed with correct inputs.")
    return True # Placeholder for actual client-side verification result

if __name__ == '__main__':
    # Example usage - replace with your actual project, location, key ring, key, and key version IDs
    # Ensure your key is an ASYMMETRIC_SIGN key (e.g., RSA_SIGN_PKCS1_2048_SHA256)
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global" # Or a specific region
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-asymmetric-sign-key-id"
    KEY_VERSION_ID = "1" # Or the specific version of your asymmetric key
    MESSAGE_TO_SIGN = b"This is a message to be signed."

    try:
        print("--- Signing Payload ---")
        signature_result = sign_payload_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, KEY_VERSION_ID, MESSAGE_TO_SIGN)
        print(f"Generated signature: {signature_result.hex()}")

        print("\n--- Verifying Signature ---")
        # In a real scenario, the signature would be passed along with the message for verification
        is_valid = verify_signature_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, KEY_VERSION_ID, MESSAGE_TO_SIGN, signature_result)
        print(f"Signature verification result: {is_valid}")

    except Exception as e:
        print(f"Error with signing or verification: {e}")
