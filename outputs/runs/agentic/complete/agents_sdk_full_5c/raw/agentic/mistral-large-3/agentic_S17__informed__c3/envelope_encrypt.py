import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: bytes, key_id: str) -> EnvelopeEncryptionResponse:
    """
    Implements envelope encryption using AWS KMS for data key encryption.
    
    Args:
        plaintext: The plaintext bytes to encrypt.
        key_id: The AWS KMS key ID or ARN.
    
    Returns:
        EnvelopeEncryptionResponse containing ciphertext, encrypted data key, and metadata.
    """
    client = get_kms_client()
    
    # Generate a data key
    data_key_response = client.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256"
    )
    
    data_key = data_key_response["Plaintext"]
    encrypted_data_key = data_key_response["CiphertextBlob"]
    
    # Encrypt the plaintext with the data key
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(
        algorithms.AES(data_key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    
    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_data_key=encrypted_data_key,
        iv=iv,
        key_id=key_id,
        algorithm="AES_256_CBC",
        provider="aws_kms"
    )