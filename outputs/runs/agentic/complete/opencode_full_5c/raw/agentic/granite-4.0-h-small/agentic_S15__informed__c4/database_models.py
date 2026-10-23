from typing import TypedDict, List, Dict, Any


class DocumentKey(TypedDict):
    id: str  # primary identifier for the document


class DocumentRequest(TypedDict):
    id: str  # identifier (may be omitted for upserts)
    data: Dict[str, Any]  # raw user‑provided document fields
    version: int = 0  # optional optimistic‑concurrency version


class DocumentResponse(TypedDict):
    id: str  # identifier of the stored document
    data: Dict[str, Any]  # normalized document data returned
    version: int = 0  # current version (for conditional updates)


class QueryOptions(TypedDict):
    filter: Dict[str, Any] = {}  # field/value pairs to match
    sort: List[str] = []  # list of fields (prefix - for desc)
    limit: int = 0  # maximum results


class NormalizedDocument(TypedDict):
    id: str
    payload: Dict[str, Any]
    version: int = 0


class ConditionalUpdate(TypedDict):
    condition: str  # e.g., "version == 5"
    updates: Dict[str, Any]


class TranslationRequest(TypedDict):
    source_text: str
    target_lang: str = "en"


class TranslationResponse(TypedDict):
    translated_text: str


class SafetyCheckRequest(TypedDict):
    text: str
    category: str = "general"


class SafetyCheckResponse(TypedDict):
    safe: bool
    flagged_reason: str = ""


class ArchiveEntry(TypedDict):
    doc_id: str
    snapshot: Dict[str, Any]
    created_at: str  # ISO‑8601 timestamp
