import os
from google.cloud import kms_v1
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_data(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes, bytes, bytes]:
    """Encrypts data using Google Cloud KMS for the data encryption key."""
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key (DEK)
    # KMS will generate a new DEK and encrypt it with the specified key
    response = client.generate_data_encryption_key(
        request={'name': key_name, 'data_encryption_algorithm': kms_v1.DataEncryptionAlgorithm.AES_256_GCM}
    )
    encrypted_dek = response.encrypted_data_encryption_key
    plaintext_dek = response.plaintext

    # Encrypt the data with the plaintext DEK using AES-256-GCM
    cipher_algo = algorithms.AES(plaintext_dek)
    iv = os.urandom(12)  # AES-256-GCM typically uses 12-byte IV

    cipher = Cipher(cipher_algo, modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    tag = encryptor.tag

    return ciphertext, encrypted_dek, iv, tag

def decrypt_data(project_id: str, location_id: str, key_ring_id: str, key_id: str,
                 ciphertext: bytes, encrypted_dek: bytes, iv: bytes, tag: bytes) -> bytes:
    """Decrypts data using Google Cloud KMS to decrypt the data encryption key."""
    client = kms_v1.KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the DEK
    response = client.decrypt(request={'name': key_name, 'ciphertext': encrypted_dek})
    plaintext_dek = response.plaintext

    # Decrypt the data with the plaintext DEK using AES-256-GCM
    cipher_algo = algorithms.AES(plaintext_dek)
    cipher = Cipher(cipher_algo, modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_plaintext

# Example usage (placeholders for your specific values)
if __name__ == "__main__":
    # TODO: Replace with your Google Cloud project details
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # e.g., "global" or "us-central1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-key-id" # The name of the symmetric key in KMS

    original_data = b"This is a secret message that needs to be encrypted."

    print(f"Original data: {original_data.decode()}")

    try:
        # Encrypt the data
        encrypted_content, encrypted_dek_key, iv_value, tag_value = encrypt_data(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, original_data
        )
        print(f"Encrypted data (ciphertext): {encrypted_content.hex()}")
        print(f"Encrypted DEK: {encrypted_dek_key.hex()}")
        print(f"IV: {iv_value.hex()}")
        print(f"Tag: {tag_value.hex()}")

        # Decrypt the data
        decrypted_content = decrypt_data(
            PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID,
            encrypted_content, encrypted_dek_key, iv_value, tag_value
        )
        print(f"Decrypted data: {decrypted_content.decode()}")

        assert original_data == decrypted_content
        print("Encryption and decryption successful!")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated to Google Cloud (e.g., 'gcloud auth application-default login')")
        print("and that the KMS key details (PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID) are correct.")
        print("Also, ensure the service account has 'Cloud KMS CryptoKey Encrypter/Decrypter' role.")
