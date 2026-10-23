import json
import os
from google.cloud import kms_v1
from security_client import KMSClient

def envelope_encrypt(plaintext: str, key_name: str) -> dict:
    """Perform envelope encryption using Cloud KMS.

    Steps:
    1. Generate a data encryption key (DEK) client‑side.
    2. Encrypt the DEK with the Cloud KMS key (wrapped key).
    3. Encrypt the plaintext with the DEK.
    4. Return both wrapped key and ciphertext together.

    Args:
        plaintext (str): Clear text to protect.
        key_name (str): Full Cloud KMS key name.

    Returns:
        dict: {'wrappedKey': base64encoded, 'ciphertext': base64encoded, 'plaintext': plaintext (optional)}
    """
    client = KMSClient()
    # 1) Generate a random 256‑bit AES key (DEK)
    import base64, os
    dek = os.urandom(32)                     # 256‑bit AES‑GCM key
    dek_bytes = dek
    # 2) Wrap (encrypt) the DEK with the KMS key
    wrapped = client.encrypt(key_name, dek_bytes)
    # The KMS Encrypt call returns a ciphertext blob; we treat it as the wrapped key
    wrapped_b64 = base64.b64encode(wrapped).decode('utf-8')
    # 3) Encrypt plaintext with the DEK using AES‑GCM
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), associated_data=None)
    ct_b64 = base64.b64encode(ciphertext).decode('utf-8')
    nonce_b64 = base64.b64encode(nonce).decode('utf-8')
    return {
        'wrappedKey': wrapped_b64,
        'nonce': nonce_b64,
        'ciphertext': ct_b64
    }
