from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, dict):
        if "plaintext" in value:
            return normalize_bytes(value["plaintext"])
        if "ciphertext" in value:
            return normalize_bytes(value["ciphertext"])
        if "data" in value:
            return normalize_bytes(value["data"])
    return str(value).encode("utf-8")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", errors="ignore")
    return str(value)


@dataclass
class SecurityRequest:
    payload: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None


@dataclass
class SecurityResponse:
    data: Dict[str, Any]
