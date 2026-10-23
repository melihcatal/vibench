from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadEnvelope:
    plaintext: Optional[str] = None
    ciphertext: Optional[bytes] = None
    key_id: Optional[str] = None
    context: Optional[Dict[str, str]] = None


@dataclass
class OperationResult:
    ok: bool
    data: Any = None
    error: Optional[str] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def normalize_context(context: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not context:
        return {}
    return {str(k): normalize_text(v) for k, v in context.items()}
