import os
from typing import Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from security_client import get_kms_client
import boto3

def _aes_gcm_encrypt(key: bytes, plaintext: bytes) -> bytes:
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()
    return iv + encryptor.tag + ct

def envelope_encrypt(plaintext: bytes, key_id: str) -> Tuple[bytes, bytes]:
    kms_client = get_kms_client()
    data_key_resp = kms_client.generate_data_key(
        KeyId=key_id,
        KeySpec='AES_256'
    )
    plaintext_key = data_key_resp['Plaintext']
    encrypted_key = data_key_resp['CiphertextBlob']
    encrypted_data = _aes_gcm_encrypt(plaintext_key, plaintext)
    return encrypted_key, encrypted_data