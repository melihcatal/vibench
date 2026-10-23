from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


def _b64(data: bytes) -> str:
    import base64

    return base64.b64encode(data).decode("utf-8")


def _unb64(value: str) -> bytes:
    import base64

    return base64.b64decode(value.encode("utf-8"))


@dataclass
class PayloadEnvelope:
    plaintext: str
    ciphertext_blob_b64: Optional[str] = None
    key_id: Optional[str] = None
    iv_b64: Optional[str] = None
    encrypted_key_b64: Optional[str] = None
    signature_b64: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"plaintext": self.plaintext}
        if self.ciphertext_blob_b64 is not None:
            data["ciphertext_blob_b64"] = self.ciphertext_blob_b64
        if self.key_id is not None:
            data["key_id"] = self.key_id
        if self.iv_b64 is not None:
            data["iv_b64"] = self.iv_b64
        if self.encrypted_key_b64 is not None:
            data["encrypted_key_b64"] = self.encrypted_key_b64
        if self.signature_b64 is not None:
            data["signature_b64"] = self.signature_b64
        return data


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def bytes_to_b64(data: bytes) -> str:
    return _b64(data)


def b64_to_bytes(value: str) -> bytes:
    return _unb64(value)
