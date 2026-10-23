import os
from google.cloud import kms_v1
import base64
from google.protobuf import wrappers_pb2

def sign_payload(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str, message: str) -> str:
    """Signs a message using an asymmetric signing key in Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    # The message must be hashed before signing. For simplicity, we'll use plain text and assume the KMS key
    # is configured for a specific digest algorithm (e.g., SHA256).
    # In a real application, you would hash the message client-side.
    # For this example, we'll let KMS handle the hashing for a direct sign.
    # KMS sign requires a digest, not plain text directly. Let's adapt.

    # For a realistic scenario, you would hash the message locally first
    # For example, using `hashlib.sha256(message.encode('utf-8')).digest()`
    # Then pass `digest={ 'sha256': hashed_message }` to the sign method.
    # However, the KMS client `sign` method expects a `digest` field.
    # Let's mock a digest for now as the prompt is about using the service for signing.
    # The best practice is to hash locally for large messages.

    # For demonstration, assume SHA256 and provide a pre-hashed dummy value or actual hash.
    # In a real application, you'd calculate this from `message`.
    # Here, we'll just sign a digest that represents the message for KMS.
    import hashlib
    message_digest_bytes = hashlib.sha256(message.encode('utf-8')).digest()

    sign_request = {
        'name': key_version_name,
        'digest': {'sha256': message_digest_bytes},
    }

    response = client.asymmetric_sign(request=sign_request)
    return base64.b64encode(response.signature).decode('utf-8')

def verify_signature(project_id: str, location_id: str, key_ring_id: str, key_id: str, key_version_id: str, message: str, signature: str) -> bool:
    """Verifies a signature using an asymmetric public key from Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()
    key_version_name = client.crypto_key_version_path(
        project_id, location_id, key_ring_id, key_id, key_version_id
    )

    # Get the public key from KMS
    public_key_response = client.get_public_key(name=key_version_name)
    public_key_pem = public_key_response.pem

    # Use a cryptography library to verify the signature locally with the public key
    # For this, we'll use `cryptography` library.
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from cryptography.hazmat.backends import default_backend

    public_key = load_pem_public_key(public_key_pem.encode('utf-8'), backend=default_backend())

    # Re-calculate the digest of the original message
    message_digest_bytes = hashlib.sha256(message.encode('utf-8')).digest() # Ensure hashlib is imported

    signature_bytes = base64.b64decode(signature)

    try:
        public_key.verify(
            signature_bytes,
            message_digest_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False

if __name__ == '__main__':
    # Example Usage (replace with your actual values and handle authentication)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location_id = "global"  # Or your specific region
    key_ring_id = "my-key-ring"
    key_id = "my-asymmetric-sign-key"
    key_version_id = "1" # Assuming key version 1
    
    sample_message = "This is a message to be signed."

    if project_id and key_ring_id and key_id and key_version_id:
        print(f"Signing payload with Google Cloud KMS key: projects/{project_id}/locations/{location_id}/keyRings/{key_ring_id}/cryptoKeys/{key_id}/cryptoKeyVersions/{key_version_id}")
        
        signed_data = sign_payload(project_id, location_id, key_ring_id, key_id, key_version_id, sample_message)
        print(f"Signature: {signed_data}")

        print("\nVerifying signature...")
        is_valid = verify_signature(project_id, location_id, key_ring_id, key_id, key_version_id, sample_message, signed_data)
        print(f"Signature valid: {is_valid}")

        # Test with tampered message
        tampered_message = "This is a tampered message."
        is_valid_tampered = verify_signature(project_id, location_id, key_ring_id, key_id, key_version_id, tampered_message, signed_data)
        print(f"Signature valid with tampered message (expected False): {is_valid_tampered}")

    else:
        print("Please set GOOGLE_CLOUD_PROJECT, GOOGLE_KMS_KEY_RING, GOOGLE_KMS_KEY, and GOOGLE_KMS_KEY_VERSION environment variables, or hardcode values for demonstration.")
