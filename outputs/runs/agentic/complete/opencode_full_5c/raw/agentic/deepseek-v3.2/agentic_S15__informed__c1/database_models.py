from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import time


@dataclass
class DocumentUpsertRequest:
    """Request for upserting a document."""

    document_id: str
    document_data: Dict[str, Any]
    timestamp: Optional[str] = None
    created_at: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.created_at is None:
            self.created_at = self.timestamp


@dataclass
class DocumentUpsertResponse:
    """Response from upserting a document."""

    success: bool
    document_id: str
    was_created: bool = False
    was_updated: bool = False
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DocumentFetchRequest:
    """Request for fetching a document."""

    document_id: str
    consistent_read: bool = False
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DocumentFetchResponse:
    """Response from fetching a document."""

    success: bool
    document_id: str
    found: bool = False
    document_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DocumentQueryRequest:
    """Request for querying documents."""

    # Query by partition key and sort key
    partition_key: Optional[str] = None
    sort_key: Optional[str] = None
    sort_key_condition: Optional[Dict[str, Any]] = None

    # Query by field value
    field_name: Optional[str] = None
    field_value: Optional[Any] = None

    # General query parameters
    filter_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Any]] = None

    # Pagination and ordering
    limit: Optional[int] = None
    scan_index_forward: Optional[bool] = None

    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DocumentRecord:
    """A single document record from a query."""

    document_id: str
    document_data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class DocumentQueryResponse:
    """Response from querying documents."""

    success: bool
    documents: List[DocumentRecord]
    count: int = 0
    has_more: bool = False
    last_evaluated_key: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ConditionalUpdateRequest:
    """Request for conditional update of a document."""

    document_id: str
    updates: Dict[str, Any]

    # Version-based condition
    version_condition: Optional[Dict[str, Any]] = None

    # Custom condition
    condition_expression: Optional[str] = None
    expression_attribute_names: Optional[Dict[str, str]] = None
    expression_attribute_values: Optional[Dict[str, Any]] = None

    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ConditionalUpdateResponse:
    """Response from conditional update."""

    success: bool
    document_id: str
    was_updated: bool = False
    condition_failed: bool = False
    updated_document: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DocumentSummaryRequest:
    """Request for summarizing documents."""

    document_ids: List[str]
    summary_options: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class DocumentSummaryResponse:
    """Response from summarizing documents."""

    success: bool
    summaries: Dict[str, str]  # document_id -> summary
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class SafetyCheckRequest:
    """Request for safety checking document content."""

    document_id: str
    text_fields: List[str]  # Field names to check
    document_data: Dict[str, Any]
    check_types: Optional[List[str]] = None  # e.g., ['toxicity', 'hate', 'sexual']
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.check_types is None:
            self.check_types = ["toxicity", "hate", "sexual"]


@dataclass
class SafetyCheckResult:
    """Result for a single safety check."""

    field_name: str
    text: str
    is_safe: bool
    scores: Dict[str, float]  # category -> score
    reasons: Optional[List[str]] = None


@dataclass
class SafetyCheckResponse:
    """Response from safety checking."""

    success: bool
    document_id: str
    overall_safe: bool
    results: List[SafetyCheckResult]
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class TranslationRequest:
    """Request for translating document fields."""

    document_id: str
    translations: Dict[str, str]  # field_name -> target_language
    document_data: Dict[str, Any]
    source_language: Optional[str] = None  # Auto-detect if None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class TranslationResult:
    """Result for a single translation."""

    field_name: str
    original_text: str
    translated_text: str
    target_language: str
    detected_language: Optional[str] = None


@dataclass
class TranslationResponse:
    """Response from translation."""

    success: bool
    document_id: str
    results: List[TranslationResult]
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ExportArchiveRequest:
    """Request for exporting and archiving documents."""

    document_ids: List[str]
    documents: List[Dict[str, Any]]  # Full document data
    archive_format: str = "zip"  # zip, tar, etc.
    include_attachments: bool = False
    storage_path: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class ExportArchiveResponse:
    """Response from export and archive."""

    success: bool
    archive_url: Optional[str] = None
    archive_key: Optional[str] = None  # Object key in storage
    document_count: int = 0
    archive_size_bytes: Optional[int] = None
    error: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
