import os
from typing import Dict, Tuple
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import boto3
from security_client import get_kms_client

def envelope_encrypt(plaintext: str, key_id: str = None) -> Dict[str, str]:
    """Implements envelope encryption using AWS KMS for the data key and AES for content."""
    kms_client = get_kms_client()
    if key_id is None:
        key_id = os.environ.get("KMS_KEY_ID")
        if not key_id:
            raise ValueError("KMS_KEY_ID environment variable or key_id parameter must be set.")

    # 1. Generate a data key from KMS
    try:
        data_key_response = kms_client.generate_data_key(
            KeyId=key_id,
            KeySpec='AES_256'
        )
        data_key_plaintext = data_key_response['Plaintext']
        encrypted_data_key = data_key_response['CiphertextBlob']
    except Exception as e:
        raise RuntimeError(f"Failed to generate data key with KMS: {e}")

    # 2. Encrypt the actual payload with the data key locally using AES
    iv = os.urandom(16) # Initialization vector
    cipher = Cipher(algorithms.AES(data_key_plaintext), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Clean up data key in memory
    del data_key_plaintext

    return {
        "Ciphertext": ciphertext.hex(),
        "EncryptedDataKey": encrypted_data_key.hex(),
        "IV": iv.hex(),
        "KmsKeyId": key_id
    }

def envelope_decrypt(encrypted_payload: Dict[str, str]) -> str:
    """Decrypts an envelope encrypted payload."""
    kms_client = get_kms_client()

    encrypted_data_key = bytes.fromhex(encrypted_payload['EncryptedDataKey'])
    ciphertext = bytes.fromhex(encrypted_payload['Ciphertext'])
    iv = bytes.fromhex(encrypted_payload['IV'])

    # 1. Decrypt the data key using KMS
    try:
        data_key_response = kms_client.decrypt(
            CiphertextBlob=encrypted_data_key,
            KeyId=encrypted_payload['KmsKeyId'] # Specify key ID if known, or KMS infers
        )
        data_key_plaintext = data_key_response['Plaintext']
    except Exception as e:
        raise RuntimeError(f"Failed to decrypt data key with KMS: {e}")

    # 2. Decrypt the actual payload locally using AES
    cipher = Cipher(algorithms.AES(data_key_plaintext), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Clean up data key in memory
    del data_key_plaintext

    return plaintext.decode('utf-8')