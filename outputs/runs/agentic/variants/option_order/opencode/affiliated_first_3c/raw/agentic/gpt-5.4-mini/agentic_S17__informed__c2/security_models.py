from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value).strip()


def normalize_metadata(value: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {normalize_text(k): normalize_text(v) for k, v in value.items()}


@dataclass
class PayloadRequest:
    plaintext: str
    key_id: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_id: str
    metadata: Dict[str, str]


@dataclass
class AuditRecord:
    key_id: str
    operation: str
    status: str
    details: Dict[str, str]
