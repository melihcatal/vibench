from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if v is not None}


def primary_key(document_id: str) -> Dict[str, str]:
    return {"document_id": document_id}


@dataclass
class OperationResult:
    ok: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


def response_payload(
    ok: bool, data: Optional[Dict[str, Any]] = None, error: Optional[str] = None
) -> Dict[str, Any]:
    payload = {"ok": ok}
    if data is not None:
        payload["data"] = data
    if error is not None:
        payload["error"] = error
    return payload
