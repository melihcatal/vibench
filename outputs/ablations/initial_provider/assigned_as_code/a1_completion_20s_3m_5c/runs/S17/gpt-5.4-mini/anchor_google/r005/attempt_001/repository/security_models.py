from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return dict(payload)
    if hasattr(payload, "__dict__"):
        return {k: v for k, v in vars(payload).items() if not k.startswith("_")}
    return {"value": payload}


def coerce_text(payload: Any, key: str) -> str:
    data = normalize_payload(payload)
    value = data.get(key, "")
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


@dataclass
class KeyConfig:
    project_id: str
    location: str
    key_ring: str
    key_id: str
    key_name: Optional[str] = None


@dataclass
class CryptoEnvelope:
    plaintext: Optional[str] = None
    ciphertext: Optional[bytes] = None
    aad: Optional[bytes] = None
    signature: Optional[bytes] = None
    verification: Optional[bool] = None


def to_bytes(value: Any) -> bytes:
    if value is None:
        return b""
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return str(value).encode("utf-8")
