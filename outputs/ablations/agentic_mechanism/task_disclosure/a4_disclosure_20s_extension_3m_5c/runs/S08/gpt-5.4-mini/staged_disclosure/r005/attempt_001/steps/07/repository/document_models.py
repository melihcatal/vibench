from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


def _normalize_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, str)):
        return value
    return str(value)


def _normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    if not metadata:
        return {}
    return {str(k): _normalize_scalar(v) for k, v in metadata.items()}


def _normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip()


def _normalize_list(values: Optional[Sequence[Any]]) -> List[Any]:
    if not values:
        return []
    return [normalize_structure(v) for v in values]


def normalize_structure(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): normalize_structure(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize_structure(v) for v in value]
    return _normalize_scalar(value)


@dataclass(frozen=True)
class StructuredDocumentExtractionRequest:
    document: Union[str, bytes]
    schema: Mapping[str, Any]
    instructions: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        return {
            "document": self.document.decode("utf-8", errors="ignore") if isinstance(self.document, bytes) else _normalize_text(self.document),
            "schema": normalize_structure(self.schema),
            "instructions": _normalize_text(self.instructions) if self.instructions is not None else None,
            "metadata": _normalize_metadata(self.metadata),
        }


@dataclass(frozen=True)
class StructuredDocumentExtractionResponse:
    extracted: Dict[str, Any]
    confidence: Optional[float] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "StructuredDocumentExtractionResponse":
        extracted = payload.get("extracted")
        if extracted is None:
            extracted = payload.get("data", {})
        confidence = payload.get("confidence")
        warnings = payload.get("warnings", [])
        metadata = payload.get("metadata", {})
        return cls(
            extracted=normalize_structure(extracted) if isinstance(extracted, Mapping) else {},
            confidence=float(confidence) if confidence is not None else None,
            warnings=[str(w) for w in warnings] if warnings else [],
            metadata=_normalize_metadata(metadata),
        )

    def normalized(self) -> Dict[str, Any]:
        return {
            "extracted": normalize_structure(self.extracted),
            "confidence": self.confidence,
            "warnings": list(self.warnings),
            "metadata": _normalize_metadata(self.metadata),
        }


@dataclass(frozen=True)
class NormalizedDocumentField:
    name: str
    value: Any
    path: str = ""
    confidence: Optional[float] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "name": _normalize_text(self.name),
            "value": normalize_structure(self.value),
            "path": _normalize_text(self.path),
            "confidence": self.confidence,
        }


@dataclass(frozen=True)
class NormalizedDocumentExtraction:
    fields: List[NormalizedDocumentField] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_response(cls, response: StructuredDocumentExtractionResponse) -> "NormalizedDocumentExtraction":
        extracted = response.extracted
        fields: List[NormalizedDocumentField] = []

        if isinstance(extracted, Mapping):
            for key, value in extracted.items():
                fields.append(NormalizedDocumentField(name=str(key), value=value))

        return cls(fields=fields, metadata=_normalize_metadata(response.metadata))

    def normalized(self) -> Dict[str, Any]:
        return {
            "fields": [field.normalized() for field in self.fields],
            "metadata": _normalize_metadata(self.metadata),
        }
