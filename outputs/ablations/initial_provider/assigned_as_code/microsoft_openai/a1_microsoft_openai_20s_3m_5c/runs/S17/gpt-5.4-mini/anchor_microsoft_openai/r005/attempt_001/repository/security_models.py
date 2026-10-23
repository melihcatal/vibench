from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, memoryview):
        return value.tobytes()
    if isinstance(value, str):
        return value.encode("utf-8")
    return str(value).encode("utf-8")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray, memoryview)):
        return normalize_bytes(value).decode("utf-8", errors="replace")
    return str(value)


@dataclass
class PayloadRequest:
    plaintext: Any
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"plaintext": normalize_bytes(self.plaintext), "key_id": self.key_id}


@dataclass
class CiphertextResponse:
    ciphertext: bytes
    key_id: str
    algorithm: str
    iv: Optional[bytes] = None
    tag: Optional[bytes] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {"ciphertext": self.ciphertext, "key_id": self.key_id, "algorithm": self.algorithm}
        if self.iv is not None:
            data["iv"] = self.iv
        if self.tag is not None:
            data["tag"] = self.tag
        return data


@dataclass
class AuditRecord:
    event_type: str
    key_id: Optional[str] = None
    payload: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"event_type": self.event_type, "key_id": self.key_id, "payload": self.payload}
