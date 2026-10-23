import os
from google.cloud import kms_v1

def encrypt_data(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """Encrypts data using Google Cloud KMS envelope encryption.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The Cloud KMS location (e.g., "global", "us-east1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the crypto key.
        plaintext: The data to encrypt.

    Returns:
        A tuple containing the encrypted data (ciphertext) and the
        encrypted data encryption key (wrapped_key).
    """
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    encrypt_response = client.encrypt(name=name, plaintext=plaintext)
    return encrypt_response.ciphertext, encrypt_response.wrapped_key

def decrypt_data(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes, wrapped_key: bytes) -> bytes:
    """Decrypts data using Google Cloud KMS envelope encryption.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The Cloud KMS location (e.g., "global", "us-east1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the crypto key.
        ciphertext: The encrypted data.
        wrapped_key: The encrypted data encryption key.

    Returns:
        The decrypted data (plaintext).
    """
    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    decrypt_response = client.decrypt(name=name, ciphertext=ciphertext, wrapped_key=wrapped_key)
    return decrypt_response.plaintext

if __name__ == "__main__":
    # These values should be replaced with your actual Google Cloud project and KMS details
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION_ID = "global"  # Or your desired location, e.g., "us-east1"
    KEY_RING_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING_ID")
    KEY_ID = os.environ.get("GOOGLE_CLOUD_KMS_KEY_ID")

    if not all([PROJECT_ID, KEY_RING_ID, KEY_ID]):
        print("Please set the environment variables: GOOGLE_CLOUD_PROJECT_ID, GOOGLE_CLOUD_KMS_KEY_RING_ID, GOOGLE_CLOUD_KMS_KEY_ID")
    else:
        original_data = b"This is the secret data to be encrypted."

        print(f"Original data: {original_data.decode()}")

        # Encrypt the data
        encrypted_data, wrapped_key = encrypt_data(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, original_data)
        print(f"Encrypted data (ciphertext): {encrypted_data.hex()}")
        print(f"Wrapped key: {wrapped_key.hex()}")

        # Decrypt the data
        decrypted_data = decrypt_data(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, encrypted_data, wrapped_key)
        print(f"Decrypted data: {decrypted_data.decode()}")

        assert original_data == decrypted_data
        print("Encryption and decryption successful!")
