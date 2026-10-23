"""
Define local request, response, and normalization helpers for MongoDB Atlas managed NoSQL document store.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class DocumentUpsertRequest:
    """Request model for upserting a document into MongoDB Atlas."""
    collection_name: str
    document_id: str
    document: Dict[str, Any]
    version: Optional[int] = None

    def to_mongo_payload(self) -> Dict[str, Any]:
        """Convert to a MongoDB-compatible payload."""
        payload = self.document.copy()
        payload["_id"] = self.document_id
        if "_metadata" not in payload:
            payload["_metadata"] = {}
        payload["_metadata"]["version"] = self.version or 1
        now = datetime.datetime.utcnow().isoformat()
        payload["_metadata"]["updated_at"] = now
        if "created_at" not in payload["_metadata"] or not payload["_metadata"]["created_at"]:
            payload["_metadata"]["created_at"] = now
        return payload


@dataclass
class DocumentFetchRequest:
    """Request model for fetching a document by ID."""
    collection_name: str
    document_id: str


@dataclass
class DocumentQueryRequest:
    """Request model for querying documents by field or partition key."""
    collection_name: str
    field_name: str
    field_value: Any
    limit: int = 100


@dataclass
class ConditionalUpdateRequest:
    """Request model for a conditional / version-aware update."""
    collection_name: str
    document_id: str
    update_fields: Dict[str, Any]
    required_version: Optional[int] = None


@dataclass
class DocumentResponse:
    """Normalized response returned to callers after MongoDB operations."""
    id: str
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize response for external consumers."""
        result = asdict(self)
        return result


@dataclass
class DocumentListResponse:
    """Response for batched document queries."""
    documents: List[DocumentResponse] = field(default_factory=list)
    total_count: int = 0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "documents": [doc.to_dict() for doc in self.documents],
            "total_count": self.total_count,
            "error": self.error,
        }


def normalize_document_result(raw_doc: Dict[str, Any]) -> DocumentResponse:
    """Normalize a raw MongoDB Atlas document dict into a DocumentResponse."""
    doc_id = str(raw_doc.pop("_id", ""))
    metadata = raw_doc.pop("_metadata", {})
    return DocumentResponse(
        id=doc_id,
        data=raw_doc,
        metadata=metadata,
        success=True,
    )


def build_upsert_response(raw_doc: Dict[str, Any], success: bool, error: Optional[str] = None) -> DocumentResponse:
    """Build a normalized response after an upsert operation."""
    doc_id = str(raw_doc.get("_id", ""))
    metadata = raw_doc.get("_metadata", {})
    return DocumentResponse(
        id=doc_id,
        data=raw_doc,
        metadata=metadata,
        success=success,
        error=error,
    )


def build_conditional_update_result(success: bool, updated_version: Optional[int] = None, error: Optional[str] = None) -> Dict[str, Any]:
    """Build a result dict for a conditional update operation."""
    return {
        "success": success,
        "updated_version": updated_version,
        "error": error,
    }
