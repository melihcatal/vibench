import base64
import os
from typing import Union

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


def decrypt_payload(ciphertext_b64: str, key_name: str) -> bytes:
    client = kms_v1.KeyManagementServiceClient()
    ciphertext = base64.b64decode(ciphertext_b64)
    response = client.decrypt(request={"name": key_name, "ciphertext": ciphertext})
    return response.plaintext


def decrypt_payload_local_aes_gcm(ciphertext_b64: str, key_name: str) -> bytes:
    raw = base64.b64decode(ciphertext_b64)
    nonce = raw[:12]
    ciphertext = raw[12:]
    key_bytes = decrypt_payload(os.environ["GCP_KMS_ENC_KEY_B64"], key_name)
    return AESGCM(key_bytes).decrypt(nonce, ciphertext, None)
