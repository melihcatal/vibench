import base64
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from security_client import SecurityClient


def envelope_encrypt(key_id: str, plaintext: str, context=None):
    client = SecurityClient()
    data_key = client.generate_data_key(key_id, context=context)
    plaintext_key = data_key["Plaintext"]
    encrypted_key = base64.b64encode(data_key["CiphertextBlob"]).decode("ascii")
    aesgcm = AESGCM(plaintext_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(
        nonce, plaintext.encode("utf-8"), json.dumps(context or {}).encode("utf-8")
    )
    return {
        "encrypted_data_key": encrypted_key,
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }
