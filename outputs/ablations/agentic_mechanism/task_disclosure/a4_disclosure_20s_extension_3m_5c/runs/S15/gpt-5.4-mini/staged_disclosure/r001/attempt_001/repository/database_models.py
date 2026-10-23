import json
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional

from google.cloud import firestore


def _normalize_document(document: Any) -> Dict[str, Any]:
    if document is None:
        raise TypeError("document must not be None")
    if isinstance(document, str):
        document = json.loads(document)
    if not isinstance(document, Mapping):
        raise TypeError("document must be a mapping or JSON string")
    return dict(document)


def _normalize_identifier(value: Any, field_name: str = "id") -> str:
    if value is None:
        raise ValueError(f"missing {field_name}")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} cannot be empty")
    return text


@dataclass(frozen=True)
class DocumentRequest:
    collection: str
    document_id: str
    document: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_input(cls, collection: str, document_id: Any, document: Any) -> "DocumentRequest":
        return cls(
            collection=_normalize_identifier(collection, "collection"),
            document_id=_normalize_identifier(document_id, "document_id"),
            document=_normalize_document(document),
        )


@dataclass(frozen=True)
class DocumentResponse:
    collection: str
    document_id: str
    exists: bool
    document: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_snapshot(cls, collection: str, document_id: Any, snapshot: Any) -> "DocumentResponse":
        exists = bool(getattr(snapshot, "exists", False))
        payload = snapshot.to_dict() if exists and hasattr(snapshot, "to_dict") else {}
        return cls(
            collection=_normalize_identifier(collection, "collection"),
            document_id=_normalize_identifier(document_id, "document_id"),
            exists=exists,
            document=dict(payload or {}),
        )


@dataclass(frozen=True)
class NormalizedDocument:
    data: Dict[str, Any]

    @classmethod
    def from_any(cls, document: Any) -> "NormalizedDocument":
        return cls(data=_normalize_document(document))

    def with_identifier(self, field_name: str = "id") -> "NormalizedDocument":
        payload = dict(self.data)
        identifier = _normalize_identifier(payload.get(field_name), field_name)
        payload[field_name] = identifier
        return NormalizedDocument(data=payload)


def build_upsert_request(collection: str, document_id: Any, document: Any) -> DocumentRequest:
    normalized = NormalizedDocument.from_any(document).with_identifier("id")
    return DocumentRequest.from_input(collection, document_id, normalized.data)


def build_fetch_response(collection: str, document_id: Any, snapshot: Any) -> DocumentResponse:
    return DocumentResponse.from_snapshot(collection, document_id, snapshot)


def to_firestore_payload(document: Any) -> Dict[str, Any]:
    return NormalizedDocument.from_any(document).data
