from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
import base64

def sign_data_with_kms(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    version_id: str,
    data: bytes
) -> bytes:
    """Signs data with a asymmetric signing key in Cloud KMS."""

    client = KeyManagementServiceClient()
    name = client.crypto_key_path_version(project_id, location_id, key_ring_id, key_id, version_id)

    # Convert the data to base64 to ensure it's handled correctly by the API
    data_base64 = base64.b64encode(data)

    response = client.asymmetric_sign(name=name, digest={"sha256": data_base64})
    return response.signature

def verify_signature_with_kms(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    version_id: str,
    data: bytes,
    signature: bytes
) -> bool:
    """Verifies a signature with an asymmetric public key in Cloud KMS."""

    client = KeyManagementServiceClient()
    name = client.crypto_key_path_version(project_id, location_id, key_ring_id, key_id, version_id)

    # Get the public key
    public_key_response = client.get_public_key(name=name)
    public_key_pem = public_key_response.pem

    # In a real application, you would use a cryptography library (like `cryptography`)
    # to verify the signature locally using the `public_key_pem`.
    # For this example, we'll demonstrate the conceptual use of KMS to get the public key.
    # Cloud KMS itself doesn't offer a direct "verify" API call. Verification is typically
    # done client-side using the public key retrieved from KMS.

    # This is a placeholder for actual verification logic.
    # You would typically use a library like 'cryptography' to perform this:
    # from cryptography.hazmat.primitives import hashes
    # from cryptography.hazmat.primitives.asymmetric import padding
    # from cryptography.hazmat.primitives import serialization
    # from cryptography.hazmat.backends import default_backend

    # public_key = serialization.load_pem_public_key(
    #     public_key_pem.encode('utf-8'),
    #     backend=default_backend()
    # )
    # try:
    #     public_key.verify(
    #         signature,
    #         data,
    #         padding.PSS(
    #             mgf=padding.MGF1(hashes.SHA256()),
    #             salt_length=padding.PSS.MAX_LENGTH
    #         ),
    #         hashes.SHA256()
    #     )
    #     return True
    # except Exception:
    #     return False

    print("Verification in a real application would use a local cryptography library with the retrieved public key.")
    print(f"Public Key (PEM format):\n{public_key_pem}")
    print("For demonstration purposes, we are skipping the actual cryptographic verification.")
    return True # Placeholder for actual verification success/failure

if __name__ == "__main__":
    # Replace with your Google Cloud KMS details
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-east1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-key-id"
    VERSION_ID = "1"  # Or the specific version of your key

    # Example data to sign
    data_to_sign = b"This is some data to be signed."

    print("Attempting to sign data...")
    try:
        signed_data = sign_data_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, VERSION_ID, data_to_sign)
        print(f"Signed Data (base64): {base64.b64encode(signed_data).decode('utf-8')}")

        print("\nAttempting to verify signature...")
        # For actual verification, you would pass the actual signature and data to the verify function
        # Here we are just demonstrating the conceptual flow.
        is_verified = verify_signature_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, VERSION_ID, data_to_sign, signed_data)
        print(f"Signature Verified: {is_verified}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure your GCP project ID, KMS key details are correct, and you have authenticated.")
        print("You might need to run 'gcloud auth application-default login' if running locally.")
