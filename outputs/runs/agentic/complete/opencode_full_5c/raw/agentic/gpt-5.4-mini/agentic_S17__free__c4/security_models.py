from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value).strip()


def normalize_key_id(value: Any) -> str:
    return normalize_text(value)


def normalize_metadata(value: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(value or {})


@dataclass
class KeyRequest:
    key_id: str
    payload: str
    aad: str = ""


@dataclass
class KeyResponse:
    key_id: str
    ciphertext: str = ""
    plaintext: str = ""
    signature: str = ""
    verified: bool = False
