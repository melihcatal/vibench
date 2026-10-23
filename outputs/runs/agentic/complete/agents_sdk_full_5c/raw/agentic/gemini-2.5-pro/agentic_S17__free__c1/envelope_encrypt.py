
import os
from cryptography.fernet import Fernet
from google.cloud import kms_v1
from security_client import get_google_kms_client
from security_models import EnvelopeEncryptResponse, EnvelopeDecryptRequest

def generate_data_key():
    """Generates a local symmetric key."""
    return Fernet.generate_key()

def encrypt_data_key(key_name: str, data_key: bytes) -> bytes:
    """Encrypts the data key with a Google Cloud KMS key."""
    client = get_google_kms_client()
    response = client.encrypt(
        request={"name": key_name, "plaintext": data_key}
    )
    return response.ciphertext

def decrypt_data_key(key_name: str, encrypted_data_key: bytes) -> bytes:
    """Decrypts the data key with a Google Cloud KMS key."""
    client = get_google_kms_client()
    response = client.decrypt(
        request={"name": key_name, "ciphertext": encrypted_data_key}
    )
    return response.plaintext

def envelope_encrypt_gcp(key_name: str, plaintext: bytes) -> EnvelopeEncryptResponse:
    """Performs envelope encryption using Google Cloud KMS."""
    data_key = generate_data_key()
    f = Fernet(data_key)
    ciphertext = f.encrypt(plaintext)
    
    encrypted_data_key = encrypt_data_key(key_name, data_key)
    
    return EnvelopeEncryptResponse(
        ciphertext=ciphertext,
        encrypted_data_key=encrypted_data_key
    )

def envelope_decrypt_gcp(key_name: str, request: EnvelopeDecryptRequest) -> bytes:
    """Performs envelope decryption using Google Cloud KMS."""
    decrypted_data_key = decrypt_data_key(key_name, request.encrypted_data_key)
    f = Fernet(decrypted_data_key)
    plaintext = f.decrypt(request.ciphertext)
    return plaintext
