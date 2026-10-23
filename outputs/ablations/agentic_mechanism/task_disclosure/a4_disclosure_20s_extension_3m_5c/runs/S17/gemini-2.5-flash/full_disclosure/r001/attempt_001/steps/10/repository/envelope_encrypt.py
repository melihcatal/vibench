from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
import os

def generate_and_wrap_dek(project_id: str, location_id: str, key_ring_id: str, key_id: str) -> tuple[bytes, bytes]:
    """
    Generates a data encryption key (DEK) and encrypts it with a Google Cloud KMS key.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring and key (e.g., 'global', 'us-central1').
        key_ring_id: The ID of the key ring.
        key_id: The ID of the symmetric encryption key in KMS (KEK).

    Returns:
        A tuple containing:
            - The plaintext data encryption key (DEK). This key should be used to encrypt actual data.
            - The encrypted (wrapped) data encryption key (DEK). This should be stored alongside the encrypted data.
    """
    client = KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Ask KMS to generate a data encryption key (DEK) and encrypt it with the KEK.
    # KMS returns both the plaintext DEK and the encrypted (wrapped) DEK.
    generate_dek_response = client.generate_data_encryption_key(request={
        "name": name,
        "key_length_bytes": 32  # For example, an AES-256 key
    })
    
    plaintext_dek = generate_dek_response.plaintext
    wrapped_dek = generate_dek_response.wrapped_key

    return plaintext_dek, wrapped_dek


def unwrap_dek(project_id: str, location_id: str, key_ring_id: str, key_id: str, wrapped_dek: bytes) -> bytes:
    """
    Decrypts an encrypted data encryption key (DEK) using a Google Cloud KMS key.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring and key.
        key_ring_id: The ID of the key ring.
        key_id: The ID of the symmetric encryption key in KMS (KEK).
        wrapped_dek: The encrypted (wrapped) data encryption key (DEK) to decrypt.

    Returns:
        The decrypted (plaintext) data encryption key (DEK). This key should be used to decrypt actual data.
    """
    client = KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the encrypted (wrapped) DEK using KMS.
    decrypt_dek_response = client.decrypt(request={
        "name": name,
        "ciphertext": wrapped_dek
    })
    
    plaintext_dek = decrypt_dek_response.plaintext

    return plaintext_dek