from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class Document:
    collection_name: str
    doc_id: str
    data: Dict[str, Any]
    version: str | None = None # Optional for optimistic locking/conditional updates

@dataclass
class QueryFilter:
    field_name: str
    operator: str  # e.g., "==", ">", "<", "array_contains"
    value: Any

@dataclass
class UpdateOperation:
    field: str
    value: Any
