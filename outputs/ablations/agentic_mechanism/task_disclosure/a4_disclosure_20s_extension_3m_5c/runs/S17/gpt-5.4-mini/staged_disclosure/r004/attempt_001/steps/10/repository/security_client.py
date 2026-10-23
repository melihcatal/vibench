import base64
import os
from dataclasses import dataclass
from typing import Optional

import requests


GOOGLE_KMS_BASE_URL = "https://cloudkms.googleapis.com/v1"
GOOGLE_OAUTH_ACCESS_TOKEN_ENV = "GOOGLE_OAUTH_ACCESS_TOKEN"
GOOGLE_CLOUD_KMS_KEY_NAME_ENV = "GOOGLE_CLOUD_KMS_KEY_NAME"


@dataclass(frozen=True)
class SecurityConfig:
    key_name: str
    access_token: str
    base_url: str = GOOGLE_KMS_BASE_URL


def load_security_config(key_name: Optional[str] = None, access_token: Optional[str] = None) -> SecurityConfig:
    resolved_key_name = key_name or os.environ.get(GOOGLE_CLOUD_KMS_KEY_NAME_ENV)
    if not resolved_key_name:
        raise ValueError(f"{GOOGLE_CLOUD_KMS_KEY_NAME_ENV} is required")

    resolved_access_token = access_token or os.environ.get(GOOGLE_OAUTH_ACCESS_TOKEN_ENV)
    if not resolved_access_token:
        raise ValueError(f"{GOOGLE_OAUTH_ACCESS_TOKEN_ENV} is required")

    return SecurityConfig(key_name=resolved_key_name, access_token=resolved_access_token)


class SecurityClient:
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or load_security_config()

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
        }

    def encrypt(self, plaintext: bytes) -> str:
        if not isinstance(plaintext, (bytes, bytearray)):
            raise TypeError("plaintext must be bytes")

        url = f"{self.config.base_url}/{self.config.key_name}:encrypt"
        response = requests.post(url, headers=self._headers(), json={"plaintext": base64.b64encode(bytes(plaintext)).decode("ascii")}, timeout=30)
        response.raise_for_status()
        return response.json()["ciphertext"]

    def decrypt(self, ciphertext_b64: str) -> bytes:
        url = f"{self.config.base_url}/{self.config.key_name}:decrypt"
        response = requests.post(url, headers=self._headers(), json={"ciphertext": ciphertext_b64}, timeout=30)
        response.raise_for_status()
        return base64.b64decode(response.json()["plaintext"])
