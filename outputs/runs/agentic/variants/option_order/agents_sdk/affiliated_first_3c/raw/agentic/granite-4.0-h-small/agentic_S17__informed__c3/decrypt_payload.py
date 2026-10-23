import os
from security_client import kms_client
import base64
from Crypto.Cipher import AES

def decrypt_payload(payload: dict) -> str:
    """Decrypt payload that was encrypted with encrypt_payload using AWS KMS.
    Args:
        payload: dict containing 'ciphertext', 'iv', 'tag', and 'encrypted_data_key'.
    Returns:
        The original plaintext string.
    """
    # Decrypt the encrypted data key using KMS
    data_key_bytes = kms_client.decrypt(
        CiphertextBlob=base64.b64decode(payload['encrypted_data_key'])
    )['Plaintext']
    # Derive AES key from the plaintext data key (same as encrypt side)
    import hashlib
    aes_key = hashlib.sha256(data_key_bytes).digest()
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(payload['iv']))
    plaintext_bytes = cipher.decrypt_and_verify(
        base64.b64decode(payload['ciphertext']),
        base64.b64decode(payload['tag'])
    )
    return plaintext_bytes.decode('utf-8')
