from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _coerce_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value.strip()))
        except ValueError:
            return None
    return None


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return False


def _ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


@dataclass
class DocumentExtractionRequest:
    document_id: Optional[str] = None
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    source_url: Optional[str] = None
    content_text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentExtractionRequest":
        return cls(
            document_id=_coerce_str(data.get("document_id")) or None,
            file_name=_coerce_str(data.get("file_name")) or None,
            mime_type=_coerce_str(data.get("mime_type")) or None,
            source_url=_coerce_str(data.get("source_url")) or None,
            content_text=_coerce_str(data.get("content_text")) or None,
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass
class ExtractedField:
    name: str
    value: Any = None
    confidence: Optional[float] = None
    page: Optional[int] = None
    normalized_value: Any = None
    raw_value: Any = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExtractedField":
        return cls(
            name=_coerce_str(data.get("name")),
            value=data.get("value"),
            confidence=_coerce_float(data.get("confidence")),
            page=_coerce_int(data.get("page")),
            normalized_value=data.get("normalized_value"),
            raw_value=data.get("raw_value", data.get("value")),
        )

    def normalize(self) -> "ExtractedField":
        if self.normalized_value is None and isinstance(self.value, str):
            self.normalized_value = self.value.strip()
        if self.raw_value is None:
            self.raw_value = self.value
        return self


@dataclass
class PageSpan:
    page: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PageSpan":
        return cls(
            page=_coerce_int(data.get("page")),
            start=_coerce_int(data.get("start")),
            end=_coerce_int(data.get("end")),
        )


@dataclass
class StructuredDocumentExtractionResponse:
    document_id: Optional[str] = None
    status: str = "unknown"
    fields: List[ExtractedField] = field(default_factory=list)
    spans: List[PageSpan] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructuredDocumentExtractionResponse":
        fields = [
            ExtractedField.from_dict(item).normalize()
            for item in _ensure_list(data.get("fields"))
            if isinstance(item, dict)
        ]
        spans = [
            PageSpan.from_dict(item)
            for item in _ensure_list(data.get("spans"))
            if isinstance(item, dict)
        ]
        warnings = [_coerce_str(item) for item in _ensure_list(data.get("warnings")) if item is not None]
        return cls(
            document_id=_coerce_str(data.get("document_id")) or None,
            status=_coerce_str(data.get("status")) or "unknown",
            fields=fields,
            spans=spans,
            warnings=warnings,
            error=_coerce_str(data.get("error")) or None,
            metadata=dict(data.get("metadata") or {}),
        )


def normalize_extracted_field(field: Dict[str, Any] | ExtractedField) -> ExtractedField:
    if isinstance(field, ExtractedField):
        return field.normalize()
    return ExtractedField.from_dict(field).normalize()


def normalize_extraction_response(data: Dict[str, Any] | StructuredDocumentExtractionResponse) -> StructuredDocumentExtractionResponse:
    if isinstance(data, StructuredDocumentExtractionResponse):
        data.fields = [normalize_extracted_field(field) for field in data.fields]
        return data
    return StructuredDocumentExtractionResponse.from_dict(data)
