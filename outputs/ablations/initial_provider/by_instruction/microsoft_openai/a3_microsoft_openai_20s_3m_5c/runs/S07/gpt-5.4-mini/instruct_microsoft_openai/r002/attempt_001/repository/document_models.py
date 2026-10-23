import base64
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


@dataclass
class DocumentRequest:
    source: str
    language: Optional[str] = None
    features: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    provider: str
    text: str = ""
    pages: List[Dict[str, Any]] = field(default_factory=list)
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    key_values: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text_response(payload: Dict[str, Any]) -> DocumentResponse:
    text = payload.get("text") or payload.get("content") or ""
    return DocumentResponse(provider=_to_text(payload.get("provider") or "openai"), text=_to_text(text), raw=payload)


def normalize_layout_response(payload: Dict[str, Any]) -> DocumentResponse:
    return DocumentResponse(
        provider=_to_text(payload.get("provider") or "microsoft-azure-ai-document-intelligence"),
        text=_to_text(payload.get("text") or ""),
        pages=list(payload.get("pages") or []),
        blocks=list(payload.get("blocks") or []),
        tables=list(payload.get("tables") or []),
        key_values=list(payload.get("key_values") or []),
        raw=payload,
    )


def normalize_table_response(payload: Dict[str, Any]) -> DocumentResponse:
    normalized = normalize_layout_response(payload)
    normalized.tables = list(payload.get("tables") or payload.get("tableResults") or [])
    return normalized


def normalize_key_value_response(payload: Dict[str, Any]) -> DocumentResponse:
    normalized = normalize_layout_response(payload)
    normalized.key_values = list(payload.get("key_values") or payload.get("keyValuePairs") or [])
    return normalized


def encode_source_to_data_uri(source: str) -> str:
    if source.startswith("data:"):
        return source
    if source.startswith("http://") or source.startswith("https://"):
        return source
    with open(source, "rb") as handle:
        data = base64.b64encode(handle.read()).decode("ascii")
    return f"data:application/octet-stream;base64,{data}"
