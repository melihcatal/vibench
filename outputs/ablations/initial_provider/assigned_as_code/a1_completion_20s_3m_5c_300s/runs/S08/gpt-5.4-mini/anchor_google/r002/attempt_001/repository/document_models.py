from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_bytes: bytes
    mime_type: str
    metadata: Dict[str, Any]


@dataclass
class DocumentField:
    name: str
    value: Optional[str]
    confidence: Optional[float] = None


def build_request(payload, default_mime_type: str = "application/pdf"):
    return DocumentRequest(
        document_bytes=payload.get("document_bytes", b""),
        mime_type=payload.get("mime_type", default_mime_type),
        metadata={k: v for k, v in payload.items() if k not in {"document_bytes", "mime_type"}},
    )


def normalize_fields(fields: Dict[str, Any]) -> Dict[str, Any]:
    return {k: (v.strip() if isinstance(v, str) else v) for k, v in fields.items()}


def pack_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_fields(item) for item in items]
