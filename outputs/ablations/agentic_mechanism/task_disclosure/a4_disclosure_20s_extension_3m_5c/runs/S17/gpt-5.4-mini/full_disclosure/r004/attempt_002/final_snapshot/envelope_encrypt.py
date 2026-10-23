import base64
import json
import os
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def envelope_encrypt(plaintext: str, key_name: Optional[str] = None) -> Dict[str, Any]:
    kms_client = kms_v1.KeyManagementServiceClient()
    name = key_name or _require_env("GOOGLE_CLOUD_KMS_KEY_NAME")

    dek = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)

    wrapped_dek = kms_client.encrypt(request={"name": name, "plaintext": dek}).ciphertext

    return {
        "provider": "google_cloud_kms",
        "key_name": name,
        "encryption_scheme": "envelope",
        "nonce_b64": base64.b64encode(nonce).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "wrapped_dek_b64": base64.b64encode(wrapped_dek).decode("ascii"),
    }


def main() -> None:
    plaintext = _require_env("PLAINTEXT_PAYLOAD")
    key_name = os.getenv("GOOGLE_CLOUD_KMS_KEY_NAME")
    result = envelope_encrypt(plaintext, key_name=key_name)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
