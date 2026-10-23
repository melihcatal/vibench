from google.cloud import kms_v1
from google.cloud.kms_v1.services.key_management_service import KeyManagementServiceClient
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_envelope(project_id: str, location_id: str, key_ring_id: str, key_id: str, plaintext: bytes):
    """
    Encrypts a plaintext payload using envelope encryption with Google Cloud KMS.
    Returns the ciphertext, the encrypted data encryption key (DEK), and the initialization vector (IV).
    """
    client = KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Generate a new data encryption key (DEK)
    generate_key_response = client.generate_random_bytes(
        key_name=key_name, length_bytes=32  # AES-256 key
    )
    dek = generate_key_response.data

    # Encrypt the DEK with KMS
    encrypt_dek_response = client.encrypt(
        name=key_name, plaintext=dek
    )
    encrypted_dek = encrypt_dek_response.ciphertext

    # Encrypt the plaintext with the DEK
    iv = os.urandom(16)  # AES block size
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext, encrypted_dek, iv, encryptor.tag

def decrypt_envelope(project_id: str, location_id: str, key_ring_id: str, key_id: str, ciphertext: bytes, encrypted_dek: bytes, iv: bytes, tag: bytes):
    """
    Decrypts a ciphertext payload using envelope encryption with Google Cloud KMS.
    """
    client = KeyManagementServiceClient()
    key_name = client.crypto_key_path(project_id, location_id, key_ring_id, key_id)

    # Decrypt the DEK with KMS
    decrypt_dek_response = client.decrypt(
        name=key_name, ciphertext=encrypted_dek
    )
    dek = decrypt_dek_response.plaintext

    # Decrypt the ciphertext with the DEK
    cipher = Cipher(algorithms.AES(dek), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    return plaintext
