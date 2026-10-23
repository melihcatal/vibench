import base64
import json
import os
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class EnvelopeEncryptionResult:
    wrapped_data_key: str
    nonce: str
    ciphertext: str
    key_id: str
    provider: str = "google-cloud-kms"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "key_id": self.key_id,
            "wrapped_data_key": self.wrapped_data_key,
            "nonce": self.nonce,
            "ciphertext": self.ciphertext,
        }


class GoogleCloudKMSClient:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("GOOGLE_CLOUD_KMS_API_KEY")
        self.base_url = "https://cloudkms.googleapis.com/v1"
        if not self.api_key:
            raise ValueError("GOOGLE_CLOUD_KMS_API_KEY is required")

    def encrypt(self, key_name: str, plaintext: bytes) -> bytes:
        url = f"{self.base_url}/{key_name}:encrypt"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {"plaintext": base64.b64encode(plaintext).decode("ascii")}
        response = requests.post(url, headers=headers, data=json.dumps(body), timeout=30)
        response.raise_for_status()
        data = response.json()
        return base64.b64decode(data["ciphertext"])


def _xor_stream(key: bytes, nonce: bytes, data: bytes) -> bytes:
    from hashlib import sha256

    out = bytearray()
    counter = 0
    while len(out) < len(data):
        block = sha256(key + nonce + counter.to_bytes(8, "big")).digest()
        out.extend(block)
        counter += 1
    return bytes(a ^ b for a, b in zip(data, out))


def envelope_encrypt(plaintext: bytes, key_name: str, api_key: Optional[str] = None) -> EnvelopeEncryptionResult:
    kms = GoogleCloudKMSClient(api_key=api_key)
    data_key = secrets.token_bytes(32)
    wrapped_data_key = kms.encrypt(key_name, data_key)
    nonce = secrets.token_bytes(12)
    ciphertext = _xor_stream(data_key, nonce, plaintext)
    return EnvelopeEncryptionResult(
        wrapped_data_key=base64.b64encode(wrapped_data_key).decode("ascii"),
        nonce=base64.b64encode(nonce).decode("ascii"),
        ciphertext=base64.b64encode(ciphertext).decode("ascii"),
        key_id=key_name,
    )


def main() -> None:
    import sys

    if len(sys.argv) != 3:
        raise SystemExit("usage: envelope_encrypt.py <key_name> <plaintext>")
    result = envelope_encrypt(sys.argv[2].encode("utf-8"), sys.argv[1])
    print(json.dumps(result.to_dict()))


if __name__ == "__main__":
    main()
