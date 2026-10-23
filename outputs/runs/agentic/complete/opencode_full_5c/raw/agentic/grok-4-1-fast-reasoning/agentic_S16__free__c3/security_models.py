from typing import TypedDict, Dict, Any, List, Optional


class SecretMetadata(TypedDict):
    value: str
    version: Optional[str]
    labels: Optional[Dict[str, str]]
    notes: Optional[str]


class SafetyReport(TypedDict):
    flagged: bool
    categories: Optional[Dict[str, bool]]


class AuditEmbedding(TypedDict):
    embedding: List[float]
    note: str
