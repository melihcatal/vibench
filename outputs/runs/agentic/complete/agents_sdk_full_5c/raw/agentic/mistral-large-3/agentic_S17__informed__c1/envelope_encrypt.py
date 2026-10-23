from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse

def envelope_encrypt(plaintext: bytes, key_id: str) -> EnvelopeEncryptionResponse:
    client = get_kms_client()
    request = EnvelopeEncryptionRequest(plaintext=plaintext, key_id=key_id)

    # Generate a data encryption key (DEK)
    dek_response = client.generate_data_key(
        KeyId=request.key_id,
        KeySpec='AES_256'
    )
    dek = dek_response['Plaintext']
    encrypted_dek = dek_response['CiphertextBlob']

    # Encrypt the plaintext with the DEK
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(request.plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(dek), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek,
        iv=iv,
        key_id=request.key_id
    )