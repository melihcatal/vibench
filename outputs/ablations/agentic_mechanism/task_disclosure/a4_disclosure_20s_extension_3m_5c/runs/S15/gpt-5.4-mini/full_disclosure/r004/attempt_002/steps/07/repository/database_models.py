import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Any) -> Dict[str, Any]:
    if isinstance(document, str):
        document = json.loads(document)
    if not isinstance(document, dict):
        raise TypeError("document must be a JSON object")
    return document


def normalize_primary_key(primary_key: Optional[str], default: str = "document_id") -> str:
    value = primary_key or default
    if not isinstance(value, str) or not value.strip():
        raise ValueError("primary_key must be a non-empty string")
    return value


def normalize_table_name(table_name: Optional[str], env_value: Optional[str] = None) -> str:
    value = table_name or env_value
    if not value or not isinstance(value, str):
        raise ValueError("table_name is required")
    return value


@dataclass
class DocumentRequest:
    document_id: str
    table_name: Optional[str] = None
    key_name: str = "document_id"
    region_name: Optional[str] = None

    def normalize(self) -> "DocumentRequest":
        if not self.document_id:
            raise ValueError("document_id is required")
        self.key_name = normalize_primary_key(self.key_name)
        if self.table_name is not None and not self.table_name:
            raise ValueError("table_name is required")
        return self


@dataclass
class DocumentRecordResponse:
    found: bool
    document: Optional[Dict[str, Any]]
    document_id: str
    table_name: str


@dataclass
class UpsertDocumentRequest:
    document: Dict[str, Any]
    table: str
    primary_key: str = "id"
    schema: str = "public"
    returning: str = "representation"

    def normalize(self) -> "UpsertDocumentRequest":
        self.document = normalize_document(self.document)
        self.primary_key = normalize_primary_key(self.primary_key, default="id")
        self.table = normalize_table_name(self.table)
        if self.primary_key not in self.document:
            raise ValueError(f"document must contain primary key field '{self.primary_key}'")
        return self


@dataclass
class UpsertDocumentResponse:
    document: Dict[str, Any]
    status_code: int
    inserted: bool


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any
    table_name: str
    limit: Optional[int] = None
    next_token: Optional[str] = None

    def normalize(self) -> "QueryDocumentsRequest":
        if not self.field_name:
            raise ValueError("field_name is required")
        self.table_name = normalize_table_name(self.table_name)
        if self.limit is not None and self.limit <= 0:
            raise ValueError("limit must be positive")
        return self


@dataclass
class QueryDocumentsResponse:
    items: list
    count: int
    scanned_count: Optional[int] = None
    next_token: Optional[str] = None
