from __future__ import annotations

import base64
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EncryptRequest:
    plaintext: str
    key_name: Optional[str] = None


@dataclass
class DecryptRequest:
    ciphertext: str
    key_name: Optional[str] = None


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_name: Optional[str] = None
    aad: Optional[str] = None


@dataclass
class SignVerifyRequest:
    message: str
    key_version_name: Optional[str] = None
    signature: Optional[str] = None


@dataclass
class CryptoResponse:
    data: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def _b64(value: bytes) -> str:
        return base64.b64encode(value).decode("utf-8")

    @staticmethod
    def _unb64(value: str) -> bytes:
        return base64.b64decode(value.encode("utf-8"))

    @classmethod
    def from_bytes(cls, field_name: str, value: bytes) -> "CryptoResponse":
        return cls({field_name: cls._b64(value)})

    def get_text(self, field_name: str) -> str:
        return str(self.data.get(field_name, ""))

    def get_bytes(self, field_name: str) -> bytes:
        return self._unb64(self.get_text(field_name)) if self.get_text(field_name) else b""
