from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import time
import uuid


Document = Dict[str, Any]


@dataclass
class UpsertRequest:
    document_id: str
    payload: Document
    partition_key: Optional[str] = None

    def to_cosmos_item(self) -> Document:
        item = dict(self.payload)
        item["id"] = self.document_id
        if self.partition_key is not None:
            item.setdefault("partitionKey", self.partition_key)
        item.setdefault("updatedAt", int(time.time()))
        return item


@dataclass
class FetchResponse:
    found: bool
    document: Optional[Document] = None
    etag: Optional[str] = None


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 100


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Document
    etag: Optional[str] = None
    partition_key: Optional[str] = None


@dataclass
class RecordSummary:
    document_id: str
    title: str
    summary: str
    source_language: Optional[str] = None


@dataclass
class SafetyResult:
    document_id: str
    flagged: bool
    categories: List[str] = field(default_factory=list)


@dataclass
class TranslationResult:
    document_id: str
    translated_fields: Dict[str, str]
    target_language: str


@dataclass
class ArchiveResult:
    document_id: str
    blob_url: str
    container: str
    blob_name: str


def ensure_document_id(document: Document) -> str:
    value = document.get("id") or document.get("document_id")
    if value:
        return str(value)
    generated = str(uuid.uuid4())
    document["id"] = generated
    return generated



def normalize_document(document: Document) -> Document:
    normalized = dict(document)
    if "_etag" in normalized:
        normalized["etag"] = normalized.pop("_etag")
    normalized.setdefault("id", ensure_document_id(normalized))
    return normalized



def normalize_documents(documents: Iterable[Document]) -> List[Document]:
    return [normalize_document(doc) for doc in documents]
