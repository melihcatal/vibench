from __future__ import annotations

"""Local request, response, and normalization helpers for structured document extraction."""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


def normalize_confidence(value: Any) -> float:
    try:
        numeric = float(value)
        return max(0.0, min(1.0, numeric / 100.0 if numeric > 1.0 else numeric))
    except Exception:
        return 0.0


@dataclass
class ExtractionRequest:
    source_name: str
    content_bytes: bytes
    mime_type: str = "application/pdf"
    page_count: int = 1

    def to_google_raw_document(self) -> Dict[str, Any]:
        return {"content": self.content_bytes, "mime_type": self.mime_type}

    def to_textract_document(self) -> Dict[str, Any]:
        return {"Bytes": self.content_bytes}


@dataclass
class FieldValue:
    name: str
    value: str
    confidence: float = 0.0
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResponse:
    document_type: str
    provider: str
    model_id: str
    fields: List[FieldValue]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "provider": self.provider,
            "model_id": self.model_id,
            "fields": [field.__dict__ for field in self.fields],
            "metadata": self.metadata,
        }


@dataclass
class NormalizedExpense:
    provider: str
    model_id: str
    payload: Dict[str, Any]

    @classmethod
    def from_json(cls, text: str, provider: str, model_id: str) -> "NormalizedExpense":
        return cls(provider=provider, model_id=model_id, payload=json.loads(text))


@dataclass
class ValidationResult:
    provider: str
    model_id: str
    is_valid: bool
    details: str


@dataclass
class StoredRecord:
    provider: str
    document_id: str
    status: str


def normalize_expense_payload(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True)
