from dataclasses import dataclass
from typing import Any, Dict


def serialize_document(document):
    if isinstance(document, dict):
        return {k: serialize_document(v) for k, v in document.items()}
    if isinstance(document, list):
        return [serialize_document(v) for v in document]
    return document


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]
    id_field: str = "_id"

    @classmethod
    def from_payload(cls, payload):
        return cls(document=payload, id_field=payload.get("id_field", "_id"))


@dataclass
class DocumentIdentifier:
    value: Any
    id_field: str = "_id"

    @classmethod
    def from_payload(cls, payload):
        return cls(value=payload["value"], id_field=payload.get("id_field", "_id"))


@dataclass
class DocumentQuery:
    field: str
    value: Any

    @classmethod
    def from_payload(cls, payload):
        return cls(field=payload["field"], value=payload["value"])


@dataclass
class ConditionalUpdateRequest:
    document_id: Any
    updates: Dict[str, Any]
    id_field: str = "_id"
    version_field: str = "version"
    expected_version: Any = None

    @classmethod
    def from_payload(cls, payload):
        return cls(
            document_id=payload["document_id"],
            updates=payload["updates"],
            id_field=payload.get("id_field", "_id"),
            version_field=payload.get("version_field", "version"),
            expected_version=payload.get("expected_version"),
        )
