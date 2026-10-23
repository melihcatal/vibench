import base64
import json
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_KMS_URL = "https://cloudkms.googleapis.com/v1"


def _access_token() -> str:
    token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if token:
        return token
    raise RuntimeError("GOOGLE_OAUTH_ACCESS_TOKEN is required")


def decrypt_payload(ciphertext_b64: str, key_name: str, aad_b64: Optional[str] = None) -> bytes:
    url = f"{GOOGLE_KMS_URL}/{key_name}:decrypt"
    payload: Dict[str, Any] = {"ciphertext": ciphertext_b64}
    if aad_b64 is not None:
        payload["additionalAuthenticatedData"] = aad_b64
    headers = {
        "Authorization": f"Bearer {_access_token()}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    plaintext_b64 = data["plaintext"]
    return base64.b64decode(plaintext_b64)


def main() -> None:
    ciphertext_b64 = os.environ.get("CIPHERTEXT_B64")
    key_name = os.environ.get("GOOGLE_KMS_KEY_NAME")
    aad_b64 = os.environ.get("AAD_B64")
    if not ciphertext_b64 or not key_name:
        raise RuntimeError("CIPHERTEXT_B64 and GOOGLE_KMS_KEY_NAME are required")
    plaintext = decrypt_payload(ciphertext_b64, key_name, aad_b64)
    os.write(1, plaintext)


if __name__ == "__main__":
    main()
