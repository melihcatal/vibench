from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: str
    key_reference: str


@dataclass
class PayloadResponse:
    ciphertext: str
    key_reference: str
    provider: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_mapping(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(data or {})
