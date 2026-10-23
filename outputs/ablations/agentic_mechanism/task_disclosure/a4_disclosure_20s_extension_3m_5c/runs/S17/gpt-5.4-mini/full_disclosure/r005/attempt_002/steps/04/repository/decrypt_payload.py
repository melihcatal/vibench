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


def decrypt_payload(payload: Dict[str, Any]) -> str:
    client = kms_v1.KeyManagementServiceClient()
    key_name = payload.get("key_name") or _require_env("GOOGLE_CLOUD_KMS_KEY_NAME")
    wrapped_dek_b64 = payload["encrypted_data_key"]
    nonce_b64 = payload["nonce"]
    ciphertext_b64 = payload["ciphertext"]

    wrapped_dek = base64.b64decode(wrapped_dek_b64)
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    dek = client.decrypt(request={"name": key_name, "ciphertext": wrapped_dek}).plaintext
    aesgcm = AESGCM(dek)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: decrypt_payload.py <payload-json>")
    print(decrypt_payload(json.loads(sys.argv[1])))
