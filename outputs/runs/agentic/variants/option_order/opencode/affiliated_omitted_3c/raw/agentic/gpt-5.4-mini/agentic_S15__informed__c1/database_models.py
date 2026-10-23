from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in payload.items() if v is not None}


@dataclass
class DocumentRecord:
    document_id: str
    data: Dict[str, Any]


@dataclass
class OperationResult:
    ok: bool
    document_id: str
    data: Optional[Dict[str, Any]] = None
    matched_count: int = 0
