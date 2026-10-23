from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    if isinstance(value, bytearray):
        return bytes(value)
    return str(value).encode("utf-8")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray)):
        return bytes(value).decode("utf-8", errors="replace")
    return str(value)


def payload_dict(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"value": payload}


@dataclass
class CryptoRequest:
    payload: Dict[str, Any]
    config: Optional[Dict[str, Any]] = None


@dataclass
class CryptoResponse:
    data: Dict[str, Any]
