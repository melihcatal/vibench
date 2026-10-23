import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _as_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _as_list_of_dicts(value: Any) -> List[Dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _pick(source: Dict[str, Any], *names: str) -> Any:
    for name in names:
        if name in source and source[name] not in (None, ""):
            return source[name]
    return None


@dataclass
class DocumentRequest:
    document_text: str
    schema: Dict[str, Any]
    document_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Any) -> "DocumentRequest":
        data = _as_dict(payload)
        return cls(
            document_text=str(_pick(data, "document_text", "text", "content") or ""),
            schema=_as_dict(_pick(data, "schema", "json_schema")),
            document_id=_pick(data, "document_id", "id"),
            metadata=_as_dict(_pick(data, "metadata", "context")),
        )


@dataclass
class DocumentResponse:
    extracted: Dict[str, Any]
    provider: str = "openai"
    model: str = "gpt-4.1-mini"
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "extracted": self.extracted,
            "provider": self.provider,
            "model": self.model,
            "raw": self.raw,
        }


def normalize_document_payload(payload: Any) -> Dict[str, Any]:
    data = _as_dict(payload)
    return {
        "document_id": _pick(data, "document_id", "id", "doc_id"),
        "document_type": _pick(data, "document_type", "type", "category"),
        "issue_date": _pick(data, "issue_date", "date", "created_at"),
        "merchant": _pick(data, "merchant", "vendor", "payee"),
        "total": _pick(data, "total", "amount", "grand_total"),
        "currency": _pick(data, "currency", "currency_code"),
        "items": _as_list_of_dicts(_pick(data, "items", "line_items")),
        "confidence_scores": _as_dict(_pick(data, "confidence_scores", "confidence")),
        "raw": data,
    }


def normalize_document_response(payload: Any) -> DocumentResponse:
    data = _as_dict(payload)
    extracted = _as_dict(_pick(data, "extracted", "data", "result"))
    if not extracted:
        extracted = normalize_document_payload(data)
    return DocumentResponse(
        extracted=extracted,
        provider=str(_pick(data, "provider") or "openai"),
        model=str(_pick(data, "model") or "gpt-4.1-mini"),
        raw=data,
    )


__all__ = [
    "DocumentRequest",
    "DocumentResponse",
    "normalize_document_payload",
    "normalize_document_response",
]
