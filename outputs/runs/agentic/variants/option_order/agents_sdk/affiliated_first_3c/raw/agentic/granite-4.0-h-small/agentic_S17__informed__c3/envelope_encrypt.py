import os
from security_client import kms_client
import base64

def envelope_encrypt(plaintext: str) -> dict:
    """Envelope‑encrypt a plaintext string using AWS KMS.
    Returns ciphertext and the encrypted data key.",
    response = kms_client.generate_data_key(
        KeyId=os.getenv('KMS_KEY_ID'),
        KeySpec='AES_256'
    )
    data_key = response['Plaintext']
    aes_key = data_key  # use raw data key as AES key
    from Crypto.Cipher import AES
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return {
        'ciphertext': base64.b64encode(ciphertext).decode(),
        'iv': base64.b64encode(cipher.nonce).decode(),
        'tag': base64.b64encode(tag).decode(),
        'encrypted_data_key': response['CiphertextBlob']
    }
