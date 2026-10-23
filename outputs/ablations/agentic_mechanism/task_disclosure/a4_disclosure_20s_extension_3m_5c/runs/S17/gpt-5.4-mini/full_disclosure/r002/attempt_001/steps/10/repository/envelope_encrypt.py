import base64
import json
import os
from typing import Any, Dict, Optional

from google.cloud import kms


def _load_plaintext(value: str) -> bytes:
    try:
        data = json.loads(value)
        if isinstance(data, dict):
            value = data.get("plaintext_b64") or data.get("plaintext") or data.get("payload") or value
    except json.JSONDecodeError:
        pass
    try:
        return base64.b64decode(value)
    except Exception:
        return value.encode("utf-8")


def _kms_client() -> kms.KeyManagementServiceClient:
    return kms.KeyManagementServiceClient()


def envelope_encrypt(plaintext: bytes, key_name: Optional[str] = None) -> Dict[str, Any]:
    if key_name is None:
        key_name = os.environ["GOOGLE_CLOUD_KMS_KEY_NAME"]

    client = _kms_client()
    dek = os.urandom(32)
    wrapped_dek = client.encrypt(request={"name": key_name, "plaintext": dek}).ciphertext

    keystream = (dek * ((len(plaintext) // len(dek)) + 1))[: len(plaintext)]
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, keystream))

    return {
        "provider": "google_cloud_kms",
        "key_name": key_name,
        "encrypted_dek_b64": base64.b64encode(wrapped_dek).decode("ascii"),
        "ciphertext_b64": base64.b64encode(ciphertext).decode("ascii"),
        "algorithm": "xor-stream+google-cloud-kms",
    }


def envelope_encrypt_text(plaintext: str, key_name: Optional[str] = None) -> Dict[str, Any]:
    return envelope_encrypt(plaintext.encode("utf-8"), key_name)


if __name__ == "__main__":
    payload = os.environ.get("PLAINTEXT", "")
    print(json.dumps(envelope_encrypt_text(payload)))
