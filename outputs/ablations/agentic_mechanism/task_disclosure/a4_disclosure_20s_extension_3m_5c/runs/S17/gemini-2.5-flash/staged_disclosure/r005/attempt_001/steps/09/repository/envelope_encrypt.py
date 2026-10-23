from google.cloud import kms_v1
from google.cloud.kms_v1.services.key_management_service import KeyManagementServiceClient
import os

def create_dek_and_encrypt_with_cmek(
    project_id: str, location_id: str, key_ring_id: str, key_id: str
) -> tuple[bytes, bytes]:
    """Creates a new data encryption key (DEK) and encrypts it with a customer-managed encryption key (CMEK) from KMS."""

    client = KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Use the synchronous encrypt method.
    response = client.create_ready_ciphertext_wrapped_key(name, "AES256")

    return response.wrapped_key.encrypted_key, response.wrapped_key.plaintext_crc32c

def decrypt_dek_with_cmek(
    project_id: str,
    location_id: str,
    key_ring_id: str,
    key_id: str,
    encrypted_dek: bytes,
) -> bytes:
    """Decrypts an encrypted data encryption key (DEK) using a customer-managed encryption key (CMEK) from KMS."""

    client = KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Use the synchronous decrypt method.
    response = client.decrypt(name=name, ciphertext=encrypted_dek)

    return response.plaintext

def encrypt_data_with_dek(dek: bytes, plaintext: bytes) -> bytes:
    """Encrypts data using a provided data encryption key (DEK)."""
    # In a real application, you would use a proper cryptographic library
    # like `cryptography` for AES encryption with the DEK.
    # For this example, we'll simulate it by simply returning the plaintext
    # as the "encrypted" data to focus on the KMS interaction.
    # THIS IS NOT SECURE AND SHOULD NOT BE USED IN PRODUCTION.
    return plaintext

def decrypt_data_with_dek(dek: bytes, encrypted_data: bytes) -> bytes:
    """Decrypts data using a provided data encryption key (DEK)."""
    # In a real application, you would use a proper cryptographic library
    # like `cryptography` for AES decryption with the DEK.
    # For this example, we'll simulate it by simply returning the encrypted_data
    # as the "decrypted" data to focus on the KMS interaction.
    # THIS IS NOT SECURE AND SHOULD NOT BE USED IN PRODUCTION.
    return encrypted_data

if __name__ == "__main__":
    # Replace with your Google Cloud project details
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION_ID = "global"  # Or your specific region, e.g., "us-central1"
    KEY_RING_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING_ID")
    KEY_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_ID")

    if not all([PROJECT_ID, KEY_RING_ID, KEY_ID]):
        print("Please set GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_KMS_KEY_RING_ID, and GOOGLE_CLOUD_KMS_KEY_ID environment variables.")
    else:
        print("--- Envelope Encryption Example ---")

        # 1. Create a DEK and encrypt it with CMEK
        print("1. Creating DEK and encrypting with CMEK...")
        encrypted_dek, dek_plaintext_crc32c = create_dek_and_encrypt_with_cmek(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID
        )
        print(f"   Encrypted DEK: {encrypted_dek.hex()}")

        # 2. Decrypt the DEK with CMEK
        print("2. Decrypting DEK with CMEK...")
        decrypted_dek = decrypt_dek_with_cmek(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, encrypted_dek
        )
        print(f"   Decrypted DEK (first 16 bytes): {decrypted_dek[:16].hex()}...")

        # 3. Encrypt sensitive data with the decrypted DEK
        sensitive_data = b"This is my secret data!"
        print(f"3. Encrypting sensitive data: {sensitive_data}")
        encrypted_data = encrypt_data_with_dek(decrypted_dek, sensitive_data)
        print(f"   Encrypted data: {encrypted_data}")

        # 4. Decrypt the sensitive data with the decrypted DEK
        print("4. Decrypting sensitive data...")
        decrypted_data = decrypt_data_with_dek(decrypted_dek, encrypted_data)
        print(f"   Decrypted data: {decrypted_data}")

        assert sensitive_data == decrypted_data
        print("--- Example Complete ---")
