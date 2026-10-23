
from google.cloud import kms_v1
from google.protobuf import wrappers_pb2
import base64

def create_kms_client():
    """Creates a Google Cloud KMS client."""
    return kms_v1.KeyManagementServiceClient()

def encrypt_data(project_id, location_id, key_ring_id, key_id, plaintext_data):
    """
    Encrypts data using Google Cloud KMS envelope encryption.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., 'global', 'us-central1').
        key_ring_id: The ID of your key ring.
        key_id: The ID of your symmetric encryption key.
        plaintext_data: The data to encrypt (bytes).

    Returns:
        A tuple containing:
        - The encrypted data key (bytes)
        - The ciphertext of the original data (bytes)
    """
    client = create_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key (DEK) and encrypt it with the KMS key
    # The plaintext DEK is not exposed.
    generate_dek_response = client.generate_random_bytes(
        project_id=project_id,
        location_id=location_id,
        length_bytes=32  # AES-256 key
    )
    
    # Encrypt the DEK with KMS
    encrypt_dek_response = client.encrypt(
        name=key_name,
        plaintext=generate_dek_response.random_bytes,
    )
    encrypted_dek = encrypt_dek_response.ciphertext

    # Use the plaintext DEK (returned by generateRandomBytes) to encrypt the data locally
    # Note: In a real application, you'd use a robust cryptographic library like PyNaCl or cryptography
    # to perform AES-256 GCM encryption with the DEK.
    # For demonstration, we'll just simulate this step.
    # IMPORTANT: THIS IS NOT REAL ENCRYPTION. IN A PRODUCTION APP, USE A CRYPTO LIB.
    ciphertext_data = b"simulated_ciphertext_of_" + plaintext_data # Replace with actual AES-256 GCM encryption

    return encrypted_dek, ciphertext_data

def decrypt_data(project_id, location_id, key_ring_id, key_id, encrypted_dek, ciphertext_data):
    """
    Decrypts data using Google Cloud KMS envelope encryption.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., 'global', 'us-central1').
        key_ring_id: The ID of your key ring.
        key_id: The ID of your symmetric encryption key.
        encrypted_dek: The encrypted data encryption key (bytes).
        ciphertext_data: The ciphertext of the original data (bytes).

    Returns:
        The decrypted plaintext data (bytes).
    """
    client = create_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the DEK using KMS
    decrypt_dek_response = client.decrypt(
        name=key_name,
        ciphertext=encrypted_dek
    )
    plaintext_dek = decrypt_dek_response.plaintext

    # Use the plaintext DEK to decrypt the data locally
    # Note: In a real application, you'd use a robust cryptographic library like PyNaCl or cryptography
    # to perform AES-256 GCM decryption with the DEK.
    # For demonstration, we'll just simulate this step.
    # IMPORTANT: THIS IS NOT REAL DECRYPTION. IN A PRODUCTION APP, USE A CRYPTO LIB.
    if ciphertext_data.startswith(b"simulated_ciphertext_of_"):
        plaintext_data = ciphertext_data[len(b"simulated_ciphertext_of_"):] # Replace with actual AES-256 GCM decryption
    else:
        raise ValueError("Simulated ciphertext format not recognized.")

    return plaintext_data

if __name__ == '__main__':
    # These values must be replaced with your actual GCP project, location, key ring, and key IDs.
    # For a real application, consider using environment variables or a configuration management system.
    # Example:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_LOCATION_ID="global"
    # export GCP_KEY_RING_ID="my-key-ring"
    # export GCP_KEY_ID="my-symmetric-key"

    # You would need to set up Google Cloud credentials for your environment.
    # For local development, `gcloud auth application-default login` is often used.
    # For production, service account keys or Workload Identity are common.

    PROJECT_ID = "your-gcp-project-id"  # Replace with your project ID
    LOCATION_ID = "global"              # Replace with your key ring location
    KEY_RING_ID = "my-key-ring"         # Replace with your key ring ID
    KEY_ID = "my-symmetric-key"         # Replace with your symmetric key ID

    original_data = b"This is a very secret message that needs to be encrypted."

    print("Original data:", original_data.decode())

    # Encrypt the data
    try:
        encrypted_dek_bytes, ciphertext_data_bytes = encrypt_data(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, original_data
        )

        print("\nEncryption successful!")
        print("Encrypted DEK (base64):", base64.b64encode(encrypted_dek_bytes).decode())
        print("Ciphertext data (simulated):", ciphertext_data_bytes.decode())

        # Decrypt the data
        decrypted_data_bytes = decrypt_data(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, encrypted_dek_bytes, ciphertext_data_bytes
        )

        print("\nDecryption successful!")
        print("Decrypted data:", decrypted_data_bytes.decode())

        assert original_data == decrypted_data_bytes
        print("\nOriginal and decrypted data match!")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have:")
        print("1. Replaced placeholder values for PROJECT_ID, LOCATION_ID, KEY_RING_ID, and KEY_ID.")
        print("2. Configured Google Cloud authentication (e.g., `gcloud auth application-default login`).")
        print("3. Enabled the Cloud Key Management Service (KMS) API in your GCP project.")
        print("4. Created a Key Ring and a symmetric encryption key in KMS.")
        print("5. Granted necessary permissions to the service account/user running this code to use the KMS key.")
