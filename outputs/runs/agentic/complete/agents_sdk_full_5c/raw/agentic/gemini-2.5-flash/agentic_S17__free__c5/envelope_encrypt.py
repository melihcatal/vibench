from google.cloud import kms
from security_client import get_kms_client
import os

def envelope_encrypt_with_kms(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """Performs envelope encryption using Google Cloud KMS.

    Generates a data encryption key (DEK) with KMS, encrypts the DEK with KMS (KEK),
    and then uses the plaintext DEK to encrypt the actual data client-side.
    Returns the encrypted DEK and the encrypted data.
    """
    client = get_kms_client()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Step 1: Generate a new data encryption key (DEK) and encrypt it with KMS (KEK)
    generate_dek_response = client.generate_symmetric_encryption_keys(request={
        "name": key_name,
        "generate_data_encryption_key_request": {
            "data_encryption_key_algorithm": kms.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
        }
    })

    encrypted_dek = generate_dek_response.wrapped_key
    plaintext_dek = generate_dek_response.plaintext_crc32c.encode() # This is the DEK to use for client-side encryption

    # Step 2: Use the plaintext DEK to encrypt the actual data client-side
    # For simplicity, using AES-256 GCM with os.urandom for IV (not production ready without proper key management)
    # In a real scenario, you'd use a robust crypto library like `cryptography`
    # and manage IVs/nonces securely. This is a placeholder for client-side encryption.
    # Using a simple XOR for demonstration, NOT for security.
    # For actual security, use something like: 
    # from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    # from cryptography.hazmat.backends import default_backend
    # iv = os.urandom(12) # For AES GCM
    # cipher = Cipher(algorithms.AES(plaintext_dek), modes.GCM(iv), backend=default_backend())
    # encryptor = cipher.encryptor()
    # ciphertext_data = encryptor.update(plaintext) + encryptor.finalize()
    # return encrypted_dek, iv + ciphertext_data # Store IV with ciphertext_data

    # Placeholder for actual client-side encryption (DO NOT USE IN PRODUCTION)
    # Simulating client-side encryption using a simple byte-wise XOR for illustration.
    # THIS IS NOT SECURE AND FOR DEMONSTRATION PURPOSES ONLY.
    encrypted_data = bytes([_a ^ _b for _a, _b in zip(plaintext, plaintext_dek * (len(plaintext) // len(plaintext_dek) + 1))])

    return encrypted_dek, encrypted_data

if __name__ == '__main__':
    # Example usage - replace with your actual project, location, key ring, and key IDs
    PROJECT_ID = "your-gcp-project-id"
    LOCATION_ID = "global"  # Or a specific region like "us-east1"
    KEY_RING_ID = "your-key-ring-id"
    KEY_ID = "your-symmetric-key-id" # Must be a symmetric key
    PLAINTEXT_DATA = b"This is the highly sensitive data for envelope encryption."

    try:
        encrypted_dek_result, encrypted_data_result = envelope_encrypt_with_kms(PROJECT_ID, LOCATION_ID, KEY_RING_ID, KEY_ID, PLAINTEXT_DATA)
        print(f"Encrypted DEK (wrapped key): {encrypted_dek_result.hex()}")
        print(f"Encrypted Data (client-side): {encrypted_data_result.hex()}")
    except Exception as e:
        print(f"Error performing envelope encryption: {e}")
