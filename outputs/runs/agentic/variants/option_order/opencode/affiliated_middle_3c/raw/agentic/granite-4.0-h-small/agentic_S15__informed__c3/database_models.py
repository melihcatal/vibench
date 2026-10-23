# [HELPER] database_models.py
from typing import Dict, Any, List, Optional

class DocumentRecord:
    """Normalized representation of a document retrieved from the NoSQL store.

    Provides attribute access and helper methods for downstream steps.
    """
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        # Normalize common fields (example: _id -> id, version field, etc.)
        self.id = raw.get("_id") or raw.get("id")
        self.version = raw.get("version", 0)
        self.payload = {k: v for k, v in raw.items() if k not in ("_id", "id", "version")}

    def to_dict(self) -> Dict[str, Any]:
        return self.payload

class BulkRecord:
    """Collection of DocumentRecord objects for batch handling.

    Useful for later-step aggregation, export, or safety checks.
    """
    def __init__(self, records: List[DocumentRecord]):
        self.records = records

    def to_list(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.records]

# Utility functions (could be expanded in later steps)

def normalize_response(raw_response: Any) -> Optional[DocumentRecord]:
    """Convert provider-specific raw response into normalized DocumentRecord.

    Returns None if response is empty (e.g., no document found).
    """
    if isinstance(raw_response, dict):
        return DocumentRecord(raw_response)
    return None


def extract_field(record: DocumentRecord, field_path: str) -> Any:
    """Safely extract nested field using dot notation (e.g., \"address.city\")."
    current = record.payload
    for part in field_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current