from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class DocumentRequest:
    document_id: str
    data: Dict[str, Any] = field(default_factory=dict)
    partition_key: Optional[str] = None
    version: Optional[int] = None


@dataclass
class DocumentResponse:
    document_id: str
    data: Dict[str, Any]
    partition_key: Optional[str] = None
    version: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    success: bool = False
    error: Optional[str] = None


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 50


@dataclass
class QueryResponse:
    documents: List[DocumentResponse]
    total_count: int = 0
    success: bool = False
    error: Optional[str] = None


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    condition: Optional[Dict[str, Any]] = None


@dataclass
class ConditionalUpdateResponse:
    document_id: str
    updated: bool = False
    new_version: int = 0
    error: Optional[str] = None


@dataclass
class SummaryRecord:
    document_id: str
    summary: str
    source_fields: List[str]
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class SafetyCheckResult:
    document_id: str
    field_name: str
    is_safe: bool
    flags: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TranslationRecord:
    document_id: str
    field_name: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class ArchiveRecord:
    archive_id: str
    document_id: str
    storage_path: str
    archived_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    size_bytes: int = 0
    error: Optional[str] = None


def normalize_document(
    raw_doc: Dict[str, Any], document_id: str = None
) -> Dict[str, Any]:
    doc_id = document_id or raw_doc.get("_id") or raw_doc.get("document_id")
    now = datetime.utcnow().isoformat()
    normalized = {
        "_id": doc_id,
        "data": raw_doc.get("data", raw_doc),
        "partition_key": raw_doc.get("partition_key"),
        "version": raw_doc.get("version", 0),
        "created_at": raw_doc.get("created_at", now),
        "updated_at": raw_doc.get("updated_at", now),
    }
    return normalized


def to_document_response(doc: Dict[str, Any]) -> DocumentResponse:
    return DocumentResponse(
        document_id=doc.get("_id", ""),
        data=doc.get("data", {}),
        partition_key=doc.get("partition_key"),
        version=doc.get("version", 0),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
        success=True,
    )
