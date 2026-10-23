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


def _request(method: str, url: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {_access_token()}",
        "Content-Type": "application/json",
    }
    response = requests.request(method, url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def sign_payload(message: bytes, key_name: str) -> str:
    url = f"{GOOGLE_KMS_URL}/{key_name}:asymmetricSign"
    digest = base64.b64encode(message).decode("ascii")
    response = _request("POST", url, {"digest": {"sha256": digest}})
    return response["signature"]


def verify_signature(message: bytes, signature_b64: str, public_key_name: str) -> bool:
    url = f"{GOOGLE_KMS_URL}/{public_key_name}:verify"
    digest = base64.b64encode(message).decode("ascii")
    response = _request("POST", url, {"digest": {"sha256": digest}, "signature": signature_b64})
    return bool(response.get("name")) or response.get("success", False)


def main() -> None:
    mode = os.environ.get("MODE", "sign")
    key_name = os.environ.get("GOOGLE_KMS_KEY_NAME")
    if not key_name:
        raise RuntimeError("GOOGLE_KMS_KEY_NAME is required")
    message = os.environ.get("MESSAGE", "").encode("utf-8")
    if mode == "sign":
        os.write(1, sign_payload(message, key_name).encode("utf-8"))
        return
    signature_b64 = os.environ.get("SIGNATURE_B64")
    if not signature_b64:
        raise RuntimeError("SIGNATURE_B64 is required for verify mode")
    os.write(1, json.dumps({"verified": verify_signature(message, signature_b64, key_name)}).encode("utf-8"))


if __name__ == "__main__":
    main()
