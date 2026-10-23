import os
import boto3
from security_client import get_kms_client, generate_data_key

kms_client = get_kms_client()

def envelope_encrypt(plaintext: str, key_id: str) -> dict:
    """Perform envelope encryption: generate a data encryption key (DEK), encrypt it (the KEK) with AWS KMS, then encrypt the plaintext with the plaintext DEK.",
    # 1. Generate a random data key (plaintext) using KMS
    data_key = generate_data_key(key_id, key_spec='AES_256')
    plaintext_key = data_key['Plaintext']  # this is the DEK as raw bytes
    encrypted_key = data_key['CiphertextBlob']  # encrypted with KMS (KEK)
    
    # 2. Encrypt the plaintext with the DEK using simple AES (placeholder; in production use a proper AES library)
    ciphertext = _aes_encrypt(plaintext.encode('utf-8'), plaintext_key)
    
    # 3. Package results
    return {
        'encrypted_data_key': encrypted_key,
        'iv': data_key['PlaintextIV'],  # if needed for CBC, otherwise omitted
        'ciphertext': ciphertext
    }

# Simple AES-256-CBC implementation using PyCryptodome (must be installed)
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
except ImportError:
    raise ImportError('Install pycryptodome to run envelope_encrypt: pip install pycryptodome')

def _aes_encrypt(data: bytes, key: bytes) -> bytes:
    iv = get_random_bytes(16)  # AES block size for CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # PKCS7 padding
    pad_len = 16 - (len(data) % 16)
    padded = data + bytes([pad_len]) * pad_len
    return iv + cipher.encrypt(padded)

if __name__ == "__main__":
    test_key_id = os.getenv('AWS_KMS_KEY_ID')
    if not test_key_id:
        raise RuntimeError('Set AWS_KMS_KEY_ID environment variable')
    sample = "Sensitive data that requires envelope encryption"
    envelope = envelope_encrypt(sample, test_key_id)
    print('Envelope encryption result:', envelope)
