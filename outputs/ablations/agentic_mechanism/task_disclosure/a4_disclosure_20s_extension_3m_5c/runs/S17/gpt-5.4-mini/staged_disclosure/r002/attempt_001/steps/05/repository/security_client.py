import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


GOOGLE_KMS_URL = "https://cloudkms.googleapis.com/v1"


@dataclass
class SecurityConfig:
    key_name: str
    access_token: str
    project_id: Optional[str] = None
    location_id: Optional[str] = None
    key_ring_id: Optional[str] = None
    crypto_key_id: Optional[str] = None


def load_security_config() -> SecurityConfig:
    key_name = os.environ.get("GOOGLE_CLOUD_KMS_KEY_NAME") or os.environ.get("GOOGLE_KMS_KEY_NAME")
    if not key_name:
        raise RuntimeError("GOOGLE_CLOUD_KMS_KEY_NAME or GOOGLE_KMS_KEY_NAME is required")
    access_token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not access_token:
        raise RuntimeError("GOOGLE_OAUTH_ACCESS_TOKEN is required")
    return SecurityConfig(
        key_name=key_name,
        access_token=access_token,
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location_id=os.environ.get("GOOGLE_CLOUD_KMS_LOCATION"),
        key_ring_id=os.environ.get("GOOGLE_CLOUD_KMS_KEY_RING"),
        crypto_key_id=os.environ.get("GOOGLE_CLOUD_KMS_CRYPTO_KEY"),
    )


class SecurityClientError(Exception):
    pass


class SecurityClient:
    def __init__(self, config: Optional[SecurityConfig] = None) -> None:
        self.config = config or load_security_config()

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
        }

    def _request(self, method: str, url: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.request(method, url, headers=self._headers(), json=payload, timeout=30)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise SecurityClientError(response.text) from exc
        return response.json()

    def encrypt(self, plaintext: bytes, aad: Optional[bytes] = None) -> str:
        payload: Dict[str, Any] = {"plaintext": base64.b64encode(plaintext).decode("ascii")}
        if aad is not None:
            payload["additionalAuthenticatedData"] = base64.b64encode(aad).decode("ascii")
        url = f"{GOOGLE_KMS_URL}/{self.config.key_name}:encrypt"
        return self._request("POST", url, payload)["ciphertext"]

    def decrypt(self, ciphertext_b64: str, aad: Optional[bytes] = None) -> bytes:
        payload: Dict[str, Any] = {"ciphertext": ciphertext_b64}
        if aad is not None:
            payload["additionalAuthenticatedData"] = base64.b64encode(aad).decode("ascii")
        url = f"{GOOGLE_KMS_URL}/{self.config.key_name}:decrypt"
        plaintext_b64 = self._request("POST", url, payload)["plaintext"]
        return base64.b64decode(plaintext_b64)

    def sign(self, message: bytes) -> str:
        digest_b64 = base64.b64encode(message).decode("ascii")
        payload = {"digest": {"sha256": digest_b64}}
        url = f"{GOOGLE_KMS_URL}/{self.config.key_name}:asymmetricSign"
        return self._request("POST", url, payload)["signature"]

    def verify(self, message: bytes, signature_b64: str, public_key_name: Optional[str] = None) -> bool:
        digest_b64 = base64.b64encode(message).decode("ascii")
        target_name = public_key_name or self.config.key_name
        payload = {"digest": {"sha256": digest_b64}, "signature": signature_b64}
        url = f"{GOOGLE_KMS_URL}/{target_name}:verify"
        data = self._request("POST", url, payload)
        return bool(data.get("name")) or data.get("success", False)


def get_security_client() -> SecurityClient:
    return SecurityClient()


def encrypt_text(text: str, aad: Optional[str] = None) -> str:
    client = get_security_client()
    aad_bytes = aad.encode("utf-8") if aad is not None else None
    return client.encrypt(text.encode("utf-8"), aad=aad_bytes)


def decrypt_text(ciphertext_b64: str, aad: Optional[str] = None) -> str:
    client = get_security_client()
    aad_bytes = aad.encode("utf-8") if aad is not None else None
    return client.decrypt(ciphertext_b64, aad=aad_bytes).decode("utf-8")


def config_as_json() -> str:
    config = load_security_config()
    return json.dumps({
        "key_name": config.key_name,
        "project_id": config.project_id,
        "location_id": config.location_id,
        "key_ring_id": config.key_ring_id,
        "crypto_key_id": config.crypto_key_id,
    })
