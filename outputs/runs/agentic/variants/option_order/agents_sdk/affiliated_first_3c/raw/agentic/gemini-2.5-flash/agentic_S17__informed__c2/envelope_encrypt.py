import os
from google.cloud import kms_v1
from cryptography.fernet import Fernet # For local encryption

def envelope_encrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: str) -> dict:
    """
    Implements envelope encryption using Google Cloud KMS for the data encryption key (DEK)
    and Fernet for local data encryption.
    """
    kms_client = kms_v1.KeyManagementServiceClient()
    
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)
    
    # 1. Generate a new data encryption key (DEK) for local encryption
    dek = Fernet.generate_key()
    fernet = Fernet(dek)

    # 2. Encrypt the plaintext locally with the DEK
    encrypted_data = fernet.encrypt(plaintext.encode('utf-8'))

    # 3. Encrypt the DEK with Google Cloud KMS
    encrypt_dek_response = kms_client.encrypt(request={'name': key_name, 'plaintext': dek})
    encrypted_dek = encrypt_dek_response.ciphertext

    return {
        'encrypted_data': encrypted_data,
        'encrypted_dek': encrypted_dek
    }

def envelope_decrypt(project_id: str, location_id: str, key_ring_id: str, key_id: str, encrypted_data: bytes, encrypted_dek: bytes) -> str:
    """
    Decrypts an envelope-encrypted payload.
    """
    kms_client = kms_v1.KeyManagementServiceClient()
    
    key_name = kms_client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # 1. Decrypt the DEK with Google Cloud KMS
    decrypt_dek_response = kms_client.decrypt(request={'name': key_name, 'ciphertext': encrypted_dek})
    dek = decrypt_dek_response.plaintext

    # 2. Decrypt the data locally with the DEK
    fernet = Fernet(dek)
    decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')

    return decrypted_data
