# envelope_encrypt.py
import os
from google.cloud import kms_v1
from security_client import KmsClient

def envelope_encrypt(plaintext: str, key_name: str) -> dict:
    """Performs envelope encryption: generates a data encryption key (DEK), encrypts it with a KMS key, then encrypts plaintext with DEK.

    Args:
        plaintext (str): Data to encrypt.
        key_name (str): Full resource name of the KMS CryptoKey that will protect the DEK.

    Returns:
        dict: Envelope containing encrypted DEK and DEK-encrypted ciphertext.
    """
    # Generate random DEK (AES-256)
    dek = os.urandom(32)
    plaintext_bytes = plaintext.encode('utf-8')
    # Encrypt plaintext with DEK (simple AES-256 CBC here for demo; use robust lib in production)
    from Crypto.Cipher import AES
    iv = os.urandom(16)
    cipher = AES.new(dek, AES.MODE_CBC, iv)
    padded = _pad(plaintext_bytes)
    ciphertext = cipher.encrypt(padded)
    # Encrypt the DEK with KMS (envelope)
    client = KmsClient.get_instance()
    wrapped = client.encrypt(key_name, dek)
    return {
        'ciphertext': ciphertext,
        'iv': iv,
        'wrapped_key': wrapped.ciphertext,
        'key_name': wrapped.name,
    }

def _pad(data: bytes) -> bytes:
    """PKCS#7 padding."""
    padding_len = 16 - (len(data) % 16)
    return data + bytes([padding_len] * padding_len)
