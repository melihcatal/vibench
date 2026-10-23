import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from security_client import get_kms_client
from security_models import EnvelopeEncryptionRequest, EnvelopeEncryptionResponse


def envelope_encrypt(plaintext: str, key_id: str) -> EnvelopeEncryptionResponse:
    client = get_kms_client()
    
    # Generate a data encryption key (DEK)
    dek = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    
    # Encrypt the DEK with AWS KMS
    kms_response = client.generate_data_key(
        KeyId=key_id,
        KeySpec="AES_256"
    )
    encrypted_dek = kms_response["CiphertextBlob"]
    dek_plain = kms_response["Plaintext"]
    
    # Encrypt the plaintext with the DEK
    cipher = Cipher(
        algorithms.AES(dek_plain),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    padded_plaintext = _pad_plaintext(plaintext.encode("utf-8"))
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    
    return EnvelopeEncryptionResponse(
        ciphertext=ciphertext,
        encrypted_dek=encrypted_dek,
        iv=iv,
        key_id=key_id
    )


def _pad_plaintext(data: bytes) -> bytes:
    block_size = 16
    padding = block_size - len(data) % block_size
    return data + bytes([padding] * padding)