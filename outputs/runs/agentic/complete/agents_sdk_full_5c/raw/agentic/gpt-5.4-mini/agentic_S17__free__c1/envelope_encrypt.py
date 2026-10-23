from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1

from security_client import load_config


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> dict:
    config = load_config()
    kms_name = key_id or config["kms_key_name"]
    if not kms_name:
        raise ValueError("Missing Google Cloud KMS key name")
    kms = kms_v1.KeyManagementServiceClient()
    dek = AESGCM.generate_key(bit_length=256)
    wrapped = kms.encrypt(request={"name": kms_name, "plaintext": dek}).ciphertext
    aesgcm = AESGCM(dek)
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode("utf-8"), None)
    return {
        "provider": "google_cloud_kms",
        "key_id": kms_name,
        "wrapped_dek": base64.b64encode(wrapped).decode("utf-8"),
        "nonce": base64.b64encode(iv).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
    }
