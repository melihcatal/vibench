"""
Database models helper for MongoDB Atlas managed NoSQL document store.
Defines request/response data classes and normalization helpers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    """Normalized request payload for document operations."""

    doc_id: str
    collection_name: str
    data: Dict[str, Any] = field(default_factory=dict)
    version: Optional[int] = None
    condition: Optional[Dict[str, Any]] = None
    ttl_seconds: Optional[int] = None

    def to_mongo_document(self) -> Dict[str, Any]:
        """Convert request data to MongoDB-compatible document."""
        doc = {
            "_id": self.doc_id,
            "data": self.data,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        if self.version is not None:
            doc["version"] = self.version
        if self.ttl_seconds is not None:
            doc["expire_at"] = datetime.utcnow().isoformat()
        return doc


@dataclass
class DocumentResponse:
    """Normalized response from document store operations."""

    doc_id: str
    data: Dict[str, Any]
    version: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    exists: bool = True

    @classmethod
    def from_mongo_document(cls, doc: Dict[str, Any]) -> DocumentResponse:
        """Parse a MongoDB document into a DocumentResponse."""
        return cls(
            doc_id=str(doc.get("_id", "")),
            data=doc.get("data", {}),
            version=doc.get("version"),
            created_at=doc.get("created_at"),
            updated_at=doc.get("updated_at"),
            exists=True,
        )

    @classmethod
    def not_found(cls, doc_id: str) -> DocumentResponse:
        return cls(
            doc_id=doc_id,
            data={},
            exists=False,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=str)


@dataclass
class QueryResponse:
    """Response wrapper for multi-document queries."""

    documents: List[DocumentResponse] = field(default_factory=list)
    total_count: int = 0
    has_more: bool = False

    @classmethod
    def from_mongo_cursor(
        cls, cursor, limit: Optional[int] = None
    ) -> QueryResponse:
        docs = []
        count = 0
        for doc in cursor:
            if limit and count >= limit:
                docs = docs  # stop adding but cursor may have more
                continue
            docs.append(DocumentResponse.from_mongo_document(doc))
            count += 1
        return cls(documents=docs, total_count=count)


def normalize_mongo_object_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure _id is serializable by converting ObjectId to string."""
    if "_id" in doc and not isinstance(doc["_id"], str):
        doc["_id"] = str(doc["_id"])
    return doc


def sanitize_for_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove or transform keys that MongoDB does not allow (e.g. dots, $ signs)."""
    sanitized = {}
    for key, value in data.items():
        clean_key = key.replace(".", "_").replace("$", "_dollar_")
        if isinstance(value, dict):
            sanitized[clean_key] = sanitize_for_mongo(value)
        else:
            sanitized[clean_key] = value
    return sanitized


def extract_user_text_fields(doc_data: Dict[str, Any]) -> Dict[str, str]:
    """Extract string fields from document data that may contain user-generated text."""
    text_fields = {}
    for key, value in doc_data.items():
        if isinstance(value, str) and len(value) > 0:
            text_fields[key] = value
    return text_fields


def summarize_document_fields(doc_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a summary of document fields with type counts and key stats."""
    field_types = {}
    text_lengths = {}
    for key, value in doc_data.items():
        field_types[key] = type(value).__name__
        if isinstance(value, str):
            text_lengths[key] = len(value)
        elif isinstance(value, (list, tuple)):
            field_types[key] = f"{type(value).__name__}[{len(value)}]"
    return {
        "field_count": len(doc_data),
        "field_types": field_types,
        "text_lengths": text_lengths,
    }
