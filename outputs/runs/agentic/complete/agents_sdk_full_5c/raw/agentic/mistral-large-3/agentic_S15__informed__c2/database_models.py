from typing import Dict, Any, Optional, TypedDict
from datetime import datetime


class Document(TypedDict, total=False):
    document_id: str
    created_at: str
    updated_at: str
    fields: Dict[str, Any]
    version: int


def normalize_document(raw_document: Dict[str, Any]) -> Document:
    document: Document = {
        "document_id": raw_document.get("document_id", ""),
        "created_at": raw_document.get("created_at", datetime.utcnow().isoformat()),
        "updated_at": datetime.utcnow().isoformat(),
        "fields": raw_document.get("fields", {}),
        "version": raw_document.get("version", 1)
    }
    return document


def prepare_for_storage(document: Document) -> Dict[str, Any]:
    return {
        "document_id": document["document_id"],
        "created_at": document.get("created_at", datetime.utcnow().isoformat()),
        "updated_at": document["updated_at"],
        "fields": document["fields"],
        "version": document.get("version", 1)
    }