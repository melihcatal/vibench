from google.cloud import kms_v1
from google.cloud.kms_v1 import KeyManagementServiceClient
import base64

def encrypt_with_envelope(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Encrypts plaintext using envelope encryption with Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring and key (e.g., "global").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        plaintext: The data to encrypt.

    Returns:
        A tuple containing:
        - The encrypted ciphertext (data encrypted with the data encryption key).
        - The encrypted data encryption key (wrapped by KMS).
    """
    client = KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Use KMS to generate a data encryption key and encrypt the data
    encrypt_response = client.encrypt(request={
        "name": key_name,
        "plaintext": plaintext,
    })

    return encrypt_response.ciphertext, encrypt_response.wrapped_key

def decrypt_with_envelope(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes, wrapped_key: bytes) -> bytes:
    """
    Decrypts ciphertext using envelope encryption with Google Cloud KMS.

    Args:
        project_id: Your Google Cloud project ID.
        location_id: The GCP location of the key ring and key (e.g., "global").
        key_ring_id: The ID of the key ring.
        key_id: The ID of the key.
        ciphertext: The data encrypted with the data encryption key.
        wrapped_key: The data encryption key (wrapped by KMS).

    Returns:
        The decrypted plaintext.
    """
    client = KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Use KMS to decrypt the data encryption key and then decrypt the data
    decrypt_response = client.decrypt(request={
        "name": key_name,
        "ciphertext": ciphertext,
        "wrapped_key": wrapped_key,
    })

    return decrypt_response.plaintext
