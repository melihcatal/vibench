import os
import base64

from google.cloud import kms_v1

from security_client import kms_client, kms_key_name, load_security_config


def envelope_encrypt(payload: str) -> str:
    config = load_security_config()
    client = kms_client()
    dek = os.urandom(32)
    encrypted_dek = client.encrypt(request={"name": kms_key_name(config), "plaintext": dek}).ciphertext
    ciphertext = bytes(a ^ dek[i % len(dek)] for i, a in enumerate(payload.encode("utf-8")))
    return base64.b64encode(encrypted_dek + b"." + ciphertext).decode("ascii")
