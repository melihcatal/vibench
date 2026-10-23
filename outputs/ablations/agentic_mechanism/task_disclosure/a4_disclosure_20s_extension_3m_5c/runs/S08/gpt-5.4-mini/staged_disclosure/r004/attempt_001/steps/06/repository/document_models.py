from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentExtractionFieldRequest:
    name: str
    description: Optional[str] = None
    required: bool = True
    data_type: str = "string"


@dataclass
class DocumentExtractionRequest:
    document_id: Optional[str] = None
    document_url: Optional[str] = None
    fields: List[DocumentExtractionFieldRequest] = field(default_factory=list)
    language: Optional[str] = None
    normalize: bool = True

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "fields": [
                {
                    "name": f.name,
                    "description": f.description,
                    "required": f.required,
                    "data_type": f.data_type,
                }
                for f in self.fields
            ],
            "normalize": self.normalize,
        }
        if self.document_id is not None:
            payload["document_id"] = self.document_id
        if self.document_url is not None:
            payload["document_url"] = self.document_url
        if self.language is not None:
            payload["language"] = self.language
        return payload


@dataclass
class NormalizedFieldValue:
    name: str
    value: Any
    confidence: Optional[float] = None
    raw_value: Optional[Any] = None


@dataclass
class DocumentExtractionResponse:
    document_id: Optional[str] = None
    fields: List[NormalizedFieldValue] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "DocumentExtractionResponse":
        extracted_fields = payload.get("fields") or payload.get("results") or []
        normalized_fields: List[NormalizedFieldValue] = []

        for item in extracted_fields:
            if isinstance(item, dict):
                normalized_fields.append(
                    NormalizedFieldValue(
                        name=str(item.get("name") or item.get("field") or ""),
                        value=item.get("value"),
                        confidence=item.get("confidence"),
                        raw_value=item.get("raw_value", item.get("value")),
                    )
                )

        return cls(
            document_id=payload.get("document_id") or payload.get("id"),
            fields=normalized_fields,
            raw_response=payload,
        )


def normalize_field_value(value: Any, data_type: str = "string") -> Any:
    if value is None:
        return None
    if data_type in {"string", "text"}:
        return str(value).strip()
    if data_type in {"int", "integer"}:
        return int(value)
    if data_type in {"float", "number"}:
        return float(value)
    if data_type in {"bool", "boolean"}:
        if isinstance(value, bool):
            return value
        lowered = str(value).strip().lower()
        return lowered in {"true", "1", "yes", "y", "on"}
    if data_type == "list":
        return value if isinstance(value, list) else [value]
    return value


def normalize_extraction_response(response: DocumentExtractionResponse) -> DocumentExtractionResponse:
    normalized: List[NormalizedFieldValue] = []
    for field_value in response.fields:
        normalized.append(
            NormalizedFieldValue(
                name=field_value.name.strip(),
                value=normalize_field_value(field_value.value),
                confidence=field_value.confidence,
                raw_value=field_value.raw_value,
            )
        )
    response.fields = normalized
    return response
