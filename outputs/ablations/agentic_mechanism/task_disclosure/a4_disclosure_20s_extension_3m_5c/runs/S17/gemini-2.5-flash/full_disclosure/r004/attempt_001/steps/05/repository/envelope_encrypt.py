
from google.cloud import kms_v1
import base64
import os

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Encrypts a plaintext payload using envelope encryption with Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The Cloud KMS location (e.g., "global", "us-central1").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the asymmetric encryption key.
        plaintext: The data to be encrypted.

    Returns:
        A tuple containing:
            - The encrypted data encryption key (DEK)
            - The ciphertext (encrypted plaintext)
    """

    client = kms_v1.KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key (DEK) and encrypt it with the KMS key
    # This also provides the plaintext DEK for local encryption
    response = client.generate_random_bytes(project_id=project_id, location_id=location_id, length_bytes=32) # Generate 256-bit DEK

    # Use the generated random bytes as the DEK
    data_encryption_key = response.data

    # Encrypt the plaintext locally with the DEK
    # For simplicity, using a mock AES GCM encryption here.
    # In a real application, you would use a robust cryptographic library like cryptography.io
    # and handle IVs and authentication tags properly.
    # This is a placeholder for actual symmetric encryption.
    encrypted_data = b"mock_encrypted_data_" + plaintext # Placeholder for actual encryption

    # Encrypt the DEK with the KMS key
    encrypt_dek_response = client.encrypt(request={
        "name": name,
        "plaintext": data_encryption_key
    })
    encrypted_dek = encrypt_dek_response.ciphertext

    return encrypted_dek, encrypted_data

