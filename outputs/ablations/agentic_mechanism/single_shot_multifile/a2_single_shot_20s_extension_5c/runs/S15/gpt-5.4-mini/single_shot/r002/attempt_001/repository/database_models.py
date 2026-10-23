from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_document(value: Any) -> Dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return {k: v for k, v in value.items() if v is not None}


def success_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"ok": True, "result": payload}


def error_response(message: str, code: str = "bad_request") -> Dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message}}


@dataclass
class _BaseRequest:
    error: Optional[str] = None

    @staticmethod
    def _get(mapping: Dict[str, Any], *keys: str) -> Any:
        for key in keys:
            if key in mapping:
                return mapping[key]
        return None


@dataclass
class UpsertDocumentRequest(_BaseRequest):
    document_id: str = ""
    document: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any]) -> "UpsertDocumentRequest":
        document_id = cls._get(mapping, "document_id", "id")
        document = cls._get(mapping, "document", "item")
        if not isinstance(document_id, str) or not document_id:
            return cls(error="Missing document_id")
        if document is None:
            return cls(error="Missing document payload")
        return cls(document_id=document_id, document=normalize_document(document))


@dataclass
class FetchDocumentRequest(_BaseRequest):
    document_id: str = ""

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any]) -> "FetchDocumentRequest":
        document_id = cls._get(mapping, "document_id", "id")
        if not isinstance(document_id, str) or not document_id:
            return cls(error="Missing document_id")
        return cls(document_id=document_id)


@dataclass
class QueryDocumentsRequest(_BaseRequest):
    field: str = ""
    value: Any = None

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any]) -> "QueryDocumentsRequest":
        field = cls._get(mapping, "field", "partition_key", "key")
        value = cls._get(mapping, "value", "partition_value", "match")
        if not isinstance(field, str) or not field:
            return cls(error="Missing query field")
        return cls(field=field, value=value)


@dataclass
class ConditionalUpdateRequest(_BaseRequest):
    document_id: str = ""
    updates: Dict[str, Any] = field(default_factory=dict)
    expected_version: Optional[int] = None

    @classmethod
    def from_mapping(cls, mapping: Dict[str, Any]) -> "ConditionalUpdateRequest":
        document_id = cls._get(mapping, "document_id", "id")
        updates = cls._get(mapping, "updates", "patch")
        expected_version = cls._get(mapping, "expected_version", "version")
        if not isinstance(document_id, str) or not document_id:
            return cls(error="Missing document_id")
        if updates is None or not isinstance(updates, dict):
            return cls(error="Missing updates payload")
        if expected_version is not None:
            try:
                expected_version = int(expected_version)
            except (TypeError, ValueError):
                return cls(error="expected_version must be an integer")
        return cls(document_id=document_id, updates=normalize_document(updates), expected_version=expected_version)
