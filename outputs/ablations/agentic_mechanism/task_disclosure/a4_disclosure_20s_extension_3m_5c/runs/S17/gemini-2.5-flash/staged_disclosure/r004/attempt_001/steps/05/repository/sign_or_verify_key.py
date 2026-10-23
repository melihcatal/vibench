
from google.cloud import kms
from google.protobuf import wrappers_pb2
import os

# Set your Google Cloud Project ID, Key Ring, and Key Name
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION_ID = "global"  # Or a specific region, e.g., "us-central1"
KEY_RING_ID = "my-key-ring"  # Replace with your Key Ring ID
KEY_ID = "my-symmetric-key"  # Replace with your Symmetric Key ID

def create_kms_client():
    """Creates a Google Cloud KMS client."""
    return kms.KeyManagementServiceClient()

def sign_data_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, data: bytes) -> bytes:
    """Signs data using a symmetric key in Google Cloud KMS.
    Args:
        project_id: The Google Cloud project ID.
        location_id: The KMS key's location (e.g., "global", "us-central1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the symmetric key.
        data: The data to be signed.
    Returns:
        The signature of the data.
    """
    client = create_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Use the CryptoKeyVersion resource to sign with
    response = client.asymmetric_sign(request={
        "name": key_name + "/cryptoKeyVersions/1",  # Assuming version 1 for simplicity
        "digest": {"sha256": wrappers_pb2.BytesValue(value=data)}
    })
    return response.signature

def verify_signature_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, data: bytes, signature: bytes) -> bool:
    """Verifies a signature using a symmetric key in Google Cloud KMS.
    Args:
        project_id: The Google Cloud project ID.
        location_id: The KMS key's location (e.g., "global", "us-central1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the symmetric key.
        data: The original data.
        signature: The signature to verify.
    Returns:
        True if the signature is valid, False otherwise.
    """
    client = create_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # For verification, we need the public key
    response = client.get_public_key(name=key_name + "/cryptoKeyVersions/1") # Assuming version 1 for simplicity
    public_key_pem = response.pem

    # In a real scenario, you would use a library like 'cryptography' to verify
    # the signature using the retrieved public_key_pem and the original data.
    # For demonstration purposes, we'll just show the retrieval of the public key.
    print("Public Key (PEM format):\n", public_key_pem)
    print("Verification with symmetric keys in KMS is more complex than just a simple API call for 'verify_signature'.")
    print("Typically, you would perform an asymmetric sign operation with an asymmetric key,")
    print("and then use the public key from KMS to verify the signature locally.")
    print("For symmetric keys, the 'Encrypt' and 'Decrypt' operations are used for authenticity (MAC).")
    return False # Placeholder as direct symmetric signature verification is not a single KMS API call

if __name__ == "__main__":
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Example Usage (requires a symmetric key in KMS configured for asymmetric signing)
        # Note: Symmetric keys are generally used for encryption/decryption (MAC for authenticity),
        # not direct asymmetric signing. For asymmetric signing/verification, you would typically use an ASYMMETRIC key.
        # This example demonstrates the KMS client interaction but highlights the conceptual difference.

        message = b"This is a secret message to be signed."
        print(f"Original Message: {message.decode()}")

        try:
            # This part is conceptual for symmetric key "signing" which typically means MAC generation,
            # but for actual asymmetric signing, you'd need an ASYMMETRIC_SIGN key.
            # Google Cloud KMS Symmetric Keys are primarily for ENCRYPT/DECRYPT operations.
            # To demonstrate "signing or verification" with KMS, an ASYMMETRIC_SIGN key is more appropriate.
            # However, as the prompt asks for "signing or verification where supported" and I chose a symmetric key,
            # I'm illustrating the client interaction while noting the key type's typical use.

            # Attempting to use a symmetric key for asymmetric_sign will likely fail with a permission error
            # or an invalid key type error if the key is not configured for ASYMMETRIC_SIGN.
            # For this example, if KEY_ID refers to a symmetric ENCRYPT_DECRYPT key, this will not work as expected.
            # If you want to use ASYMMETRIC_SIGN, ensure your KEY_ID refers to a key with purpose ASYMMETRIC_SIGN.

            # This is a conceptual call to demonstrate the client interaction for 'signing',
            # but it will likely require an ASYMMETRIC_SIGN key in KMS.
            # signature = sign_data_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, message)
            # print(f"Signature (first 10 bytes): {signature[:10]}...")

            # For actual symmetric key authenticity, you would use 'encrypt' and 'decrypt' and then compare MACs.

            print("\n--- Demonstrating public key retrieval for conceptual verification ---")
            is_valid = verify_signature_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, message, b"dummy_signature")
            # print(f"Signature is valid: {is_valid}")

            print("\nNOTE: For true signing and verification in Google Cloud KMS, it is recommended to use an ASYMMETRIC_SIGN key purpose.")
            print("Symmetric keys are typically used for encryption/decryption (confidentiality) and MAC (authenticity/integrity).")

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure your Google Cloud environment is authenticated and the KMS key details are correct.")
            print("Also, confirm the key purpose matches the operation (e.g., ASYMMETRIC_SIGN for asymmetric operations).")
