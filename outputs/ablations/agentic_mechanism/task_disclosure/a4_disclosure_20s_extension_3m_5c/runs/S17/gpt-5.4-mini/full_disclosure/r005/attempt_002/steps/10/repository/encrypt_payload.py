import base64
import os
from typing import Any, Dict

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def encrypt_payload(plaintext: str) -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    key_name = _require_env("GOOGLE_CLOUD_KMS_KEY_NAME")
    dek = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    wrapped_dek = client.encrypt(request={"name": key_name, "plaintext": dek}).ciphertext
    return {
        "provider": "google_cloud_kms",
        "key_name": key_name,
        "encrypted_data_key": base64.b64encode(wrapped_dek).decode("ascii"),
        "nonce": base64.b64encode(nonce).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: encrypt_payload.py <plaintext>")
    print(json.dumps(encrypt_payload(sys.argv[1])))
