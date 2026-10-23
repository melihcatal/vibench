import os
from google.cloud import kms_v1
from security_client import KmsClient

# For local data encryption
from cryptography.fernet import Fernet

def envelope_encrypt(plaintext: str, key_id: str) -> tuple[bytes, bytes, str]:
    kms_client = KmsClient()
    name = kms_client.get_key_path(key_id)

    # Generate a new data encryption key (DEK) locally
    data_key = Fernet.generate_key()
    f = Fernet(data_key)
    encrypted_data = f.encrypt(plaintext.encode("utf-8"))

    # Encrypt the DEK with Google Cloud KMS
    encrypt_dek_response = kms_client.client.encrypt(name=name, plaintext=data_key)
    encrypted_dek = encrypt_dek_response.ciphertext

    return encrypted_data, encrypted_dek, key_id
