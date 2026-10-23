import base64
from security_client import get_kms_client, get_data_key_id

def envelope_encrypt(plaintext: str) -> dict:
    """Envelope encryption: generate a data key, encrypt it with the master key, then encrypt the payload.

    Returns ciphertext_base64, encrypted_data_key_base64, and key_id.
    """
    client = get_kms_client()
    # Generate a data key
    data_key = client.generate_data_key(KeyId=get_data_key_id(), KeySpec='AES_256')
    data_key_plain = data_key['Plaintext']
    encrypted_key = data_key['CiphertextBlob']
    # Encrypt payload with the plaintext data key (simple AES example, could use PyCryptodome)
    ciphertext = encrypt_with_aes(data_key_plain, plaintext)  # placeholder local helper
    return {
        'ciphertext_base64': base64.b64encode(ciphertext).decode('utf-8'),
        'encrypted_data_key_base64': base64.b64encode(encrypted_key).decode('utf-8'),
        'key_id': get_data_key_id()
    }

# Simple AES ECB placeholder - in production use proper authenticated encryption
import os, hashlib
from Crypto.Cipher import AES

def encrypt_with_aes(key: bytes, plaintext: str) -> bytes:
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_GCM)
    ct, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return iv + cipher.nonce + tag + ct
