import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from google.cloud import kms_v1


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: str
    encrypted_dek: str
    nonce: str
    key_name: str
    provider: str = "google_cloud_kms"


def _b64e(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def _b64d(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


def _load_payload(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def encrypt_payload(payload: Any, key_name: Optional[str] = None) -> Dict[str, str]:
    key_name = key_name or os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME")
    if not key_name:
        raise ValueError("GOOGLE_CLOUD_KMS_KEY_NAME is required")

    client = kms_v1.KeyManagementServiceClient()
    dek = os.urandom(32)
    aesgcm = AESGCM(dek)
    nonce = os.urandom(12)
    plaintext = _load_payload(payload)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    encrypted_dek = client.encrypt(request={"name": key_name, "plaintext": dek}).ciphertext

    result = EnvelopeEncryptionResult(
        ciphertext=_b64e(ciphertext),
        encrypted_dek=_b64e(encrypted_dek),
        nonce=_b64e(nonce),
        key_name=key_name,
    )
    return result.__dict__


def envelope_encrypt(payload: Any, key_name: Optional[str] = None) -> Dict[str, str]:
    return encrypt_payload(payload, key_name=key_name)


def main() -> None:
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Envelope encrypt a payload using Google Cloud KMS")
    parser.add_argument("payload", help="Plaintext payload to encrypt")
    parser.add_argument("--key-name", help="Google Cloud KMS key resource name")
    args = parser.parse_args()

    result = envelope_encrypt(args.payload, key_name=args.key_name)
    sys.stdout.write(json.dumps(result, separators=(",", ":")))


if __name__ == "__main__":
    main()
