import base64
import json
import os
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


def _encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def envelope_encrypt(plaintext: str, key_name: str, associated_data: Optional[str] = None) -> Dict[str, Any]:
    client = kms_v1.KeyManagementServiceClient()
    dek = AESGCM.generate_key(bit_length=256)
    response = client.encrypt(request={"name": key_name, "plaintext": dek})
    encrypted_dek = response.ciphertext
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    aad_bytes = associated_data.encode("utf-8") if associated_data is not None else None
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), aad_bytes)
    return {
        "provider": "google_cloud_kms",
        "key_name": key_name,
        "encrypted_dek": _encode(encrypted_dek),
        "nonce": _encode(nonce),
        "ciphertext": _encode(ciphertext),
        "associated_data": associated_data,
        "algorithm": "AES-256-GCM",
    }


def main() -> None:
    plaintext = os.environ["PLAINTEXT"]
    key_name = os.environ["GCP_KMS_KEY_NAME"]
    associated_data = os.environ.get("ASSOCIATED_DATA")
    result = envelope_encrypt(plaintext=plaintext, key_name=key_name, associated_data=associated_data)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
