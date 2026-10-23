from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
from google.cloud.kms_v1.services.key_management_service import pagers
import os
import base64
from cryptography.fernet import Fernet

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Performs envelope encryption using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global").
        key_ring_id: The ID of your key ring.
        key_id: The ID of your symmetric encryption key.
        plaintext: The data to encrypt.

    Returns:
        A tuple containing the encrypted data encryption key (DEK) and the ciphertext.
    """
    client = KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key (DEK)
    generate_key_response = client.generate_data_encryption_key(
        request={'name': name, 'key_delegate': KeyManagementServiceClient.generate_data_encryption_key_path(project_id, location_id, key_ring_id, key_id), 'plaintext_aad': b'', 'data_encryption_algorithm': pagers.ListCryptoKeysPager.DATA_ENCRYPTION_ALGORITHM_AES_256_GCM}
    )
    encrypted_dek = generate_key_response.encrypted_key_data
    plaintext_dek = generate_key_response.plaintext_data_encryption_key

    # Encrypt the plaintext with the DEK
    f = Fernet(base64.urlsafe_b64encode(plaintext_dek))
    ciphertext = f.encrypt(plaintext)

    return encrypted_dek, ciphertext

def envelope_decrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, encrypted_dek: bytes, ciphertext: bytes) -> bytes:
    """
    Performs envelope decryption using Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring (e.g., "global").
        key_ring_id: The ID of your key ring.
        key_id: The ID of your symmetric encryption key.
        encrypted_dek: The encrypted data encryption key (DEK).
        ciphertext: The data to decrypt.

    Returns:
        The decrypted plaintext.
    """
    client = KeyManagementServiceClient()
    name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the DEK
    decrypt_response = client.decrypt(
        request={'name': name, 'ciphertext': encrypted_dek, 'ciphertext_aad': b''}
    )
    plaintext_dek = decrypt_response.plaintext_data_encryption_key

    # Decrypt the ciphertext with the DEK
    f = Fernet(base64.urlsafe_b64encode(plaintext_dek))
    plaintext = f.decrypt(ciphertext)

    return plaintext
