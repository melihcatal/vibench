from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from decimal import Decimal


def normalize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if isinstance(value, dict):
        return {str(k): normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    return value


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return normalize_value(document)


def normalize_document_from_item(item: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    return None if item is None else normalize_document(item)


def to_expression_value(value: Any) -> Any:
    return value


def to_dynamodb_item(document: Dict[str, Any]) -> Dict[str, Any]:
    return document


@dataclass
class UpsertDocumentRequest:
    document: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UpsertDocumentRequest":
        document = data.get("document", data)
        return cls(document=document)


@dataclass
class UpsertDocumentResponse:
    document: Dict[str, Any]
    stored: bool

    def to_dict(self) -> Dict[str, Any]:
        return {"document": self.document, "stored": self.stored}


@dataclass
class FetchDocumentRequest:
    primary_key_name: str
    primary_key_value: Any

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FetchDocumentRequest":
        return cls(
            primary_key_name=data.get("primary_key_name", "id"),
            primary_key_value=data["primary_key_value"],
        )


@dataclass
class FetchDocumentResponse:
    document: Optional[Dict[str, Any]]
    found: bool

    def to_dict(self) -> Dict[str, Any]:
        return {"document": self.document, "found": self.found}


@dataclass
class QueryDocumentsRequest:
    partition_key_name: Optional[str] = None
    partition_key_value: Any = None
    field_name: Optional[str] = None
    field_value: Any = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueryDocumentsRequest":
        return cls(
            partition_key_name=data.get("partition_key_name"),
            partition_key_value=data.get("partition_key_value"),
            field_name=data.get("field_name"),
            field_value=data.get("field_value"),
        )


@dataclass
class QueryDocumentsResponse:
    items: List[Dict[str, Any]]
    count: int

    def to_dict(self) -> Dict[str, Any]:
        return {"items": self.items, "count": self.count}


@dataclass
class ConditionalUpdateRequest:
    primary_key_name: str
    primary_key_value: Any
    update_field: str
    new_value: Any
    expected_version: Optional[int] = None
    condition_field: Optional[str] = None
    expected_value: Any = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConditionalUpdateRequest":
        return cls(
            primary_key_name=data.get("primary_key_name", "id"),
            primary_key_value=data["primary_key_value"],
            update_field=data["update_field"],
            new_value=data["new_value"],
            expected_version=data.get("expected_version"),
            condition_field=data.get("condition_field"),
            expected_value=data.get("expected_value"),
        )


@dataclass
class ConditionalUpdateResponse:
    updated: Optional[Dict[str, Any]]
    applied: bool

    def to_dict(self) -> Dict[str, Any]:
        return {"updated": self.updated, "applied": self.applied}