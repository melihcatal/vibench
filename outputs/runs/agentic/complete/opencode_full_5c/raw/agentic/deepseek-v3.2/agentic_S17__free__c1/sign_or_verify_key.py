import os
import base64
import hashlib
from google.cloud import kms_v1
from google.cloud.kms_v1 import types


def sign_data(data: str, key_name: str) -> dict:
    """Sign data using Google Cloud KMS asymmetric signing key."""
    client = kms_v1.KeyManagementServiceClient()

    # Hash the data
    data_hash = hashlib.sha256(data.encode("utf-8")).digest()

    # Create digest for signing
    digest = types.Digest()
    digest.sha256 = data_hash

    # Sign the digest
    response = client.asymmetric_sign(request={"name": key_name, "digest": digest})

    signature_b64 = base64.b64encode(response.signature).decode("utf-8")

    return {
        "signature": signature_b64,
        "key_name": key_name,
        "data_hash": base64.b64encode(data_hash).decode("utf-8"),
        "provider": "google-cloud-kms",
        "algorithm": "RSA_SIGN_PKCS1_2048_SHA256",
    }


def verify_signature(data: str, signature_b64: str, key_name: str) -> dict:
    """Verify signature using Google Cloud KMS."""
    client = kms_v1.KeyManagementServiceClient()

    # Hash the data
    data_hash = hashlib.sha256(data.encode("utf-8")).digest()

    # Create digest for verification
    digest = types.Digest()
    digest.sha256 = data_hash

    # Decode signature
    signature = base64.b64decode(signature_b64)

    # Get public key
    public_key_response = client.get_public_key(request={"name": key_name})

    # Verify signature
    try:
        # Note: KMS doesn't have a direct verify API, we would use the public key
        # For this example, we'll simulate verification
        # In practice, you'd use cryptography library with the public key
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        from cryptography.hazmat.primitives.serialization import load_pem_public_key

        public_key = load_pem_public_key(public_key_response.pem.encode("utf-8"))
        public_key.verify(
            signature, data.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
        )
        is_valid = True
    except Exception as e:
        is_valid = False

    return {
        "is_valid": is_valid,
        "key_name": key_name,
        "provider": "google-cloud-kms",
        "algorithm": "RSA_SIGN_PKCS1_2048_SHA256",
    }


if __name__ == "__main__":
    # Example usage
    key_name = os.environ.get(
        "GCP_KMS_SIGNING_KEY_NAME",
        "projects/my-project/locations/global/keyRings/my-key-ring/cryptoKeys/my-signing-key/cryptoKeyVersions/1",
    )
    data = "Important data to sign"

    signature_result = sign_data(data, key_name)
    print(f"Signature: {signature_result}")

    # Verify
    verification_result = verify_signature(
        data, signature_result["signature"], key_name
    )
    print(f"Verification: {verification_result}")
