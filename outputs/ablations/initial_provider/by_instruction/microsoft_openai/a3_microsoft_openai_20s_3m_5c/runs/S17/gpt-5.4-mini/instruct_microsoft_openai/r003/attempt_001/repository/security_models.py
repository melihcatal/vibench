from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value).strip()


@dataclass
class PayloadRequest:
    payload: str
    key_id: Optional[str] = None


@dataclass
class PayloadResponse:
    result: str
    metadata: Dict[str, Any]


def wrap_result(result: str, **metadata: Any) -> PayloadResponse:
    return PayloadResponse(result=result, metadata=metadata)
