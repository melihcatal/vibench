
import base64
from google.cloud import kms_v1

def encrypt_data_with_dek(data: bytes, dek: bytes) -> bytes:
    """Encrypts data using a data encryption key (DEK).
    This is a placeholder for actual data encryption (e.g., AES-GCM).
    For simplicity, this example just XORs the data with the DEK.
    """
    encrypted_data = bytearray(len(data))
    for i in range(len(data)):
        encrypted_data[i] = data[i] ^ dek[i % len(dek)]
    return bytes(encrypted_data)

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Performs envelope encryption using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The KMS key's location (e.g., "global", "us-central1").
        key_ring_id: The ID of the KMS key ring.
        key_id: The ID of the KMS key.
        plaintext: The data to be encrypted.

    Returns:
        A tuple containing:
        - The encrypted data encryption key (DEK) from KMS.
        - The data encrypted with the DEK.
    """
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # 1. Generate a new data encryption key (DEK) and encrypt it with KMS.
    # We request KMS to generate a new DEK and encrypt it with the specified master key.
    # The DEK size (e.g., 32 bytes for AES-256) should be chosen based on the symmetric algorithm used for data encryption.
    generate_dek_response = client.generate_random_bytes(project_id="gcp-project-id", length_bytes=32)
    plaintext_dek = generate_dek_response.data

    encrypt_dek_response = client.encrypt(name=key_name, plaintext=plaintext_dek)
    encrypted_dek = encrypt_dek_response.ciphertext

    # 2. Encrypt the actual data with the plaintext DEK.
    # In a real application, you would use a robust symmetric encryption algorithm (e.g., AES-256 GCM) here.
    # For this example, we use a simplified encryption function.
    encrypted_data = encrypt_data_with_dek(plaintext, plaintext_dek)

    return encrypted_dek, encrypted_data

if __name__ == "__main__":
    # Replace with your actual GCP project, location, key ring, and key IDs
    # For demonstration purposes, using placeholder values.
    # Ensure you have authenticated with gcloud (e.g., `gcloud auth application-default login`)
    # and have the KMS CryptoKey Encrypter/Decrypter role on the specified key.
    GCP_PROJECT_ID = "gcp-project-id"  # Replace with your project ID
    KMS_LOCATION_ID = "global"
    KMS_KEY_RING_ID = "my-key-ring"  # Replace with your key ring ID
    KMS_KEY_ID = "my-key"  # Replace with your key ID

    data_to_encrypt = b"This is a secret message that needs to be protected."

    try:
        encrypted_dek, encrypted_data = envelope_encrypt(
            GCP_PROJECT_ID, KMS_LOCATION_ID, KMS_KEY_RING_ID, KMS_KEY_ID, data_to_encrypt
        )

        print("Envelope Encryption successful!")
        print(f"Encrypted DEK (base64): {base64.b64encode(encrypted_dek).decode('utf-8')}")
        print(f"Encrypted Data (base64): {base64.b64encode(encrypted_data).decode('utf-8')}")

        # To decrypt, you would first decrypt the encrypted_dek using KMS,
        # then use the plaintext_dek to decrypt the encrypted_data.
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated with Google Cloud and have the necessary permissions.")
        print("Also, verify that the project ID, location, key ring ID, and key ID are correct.")
