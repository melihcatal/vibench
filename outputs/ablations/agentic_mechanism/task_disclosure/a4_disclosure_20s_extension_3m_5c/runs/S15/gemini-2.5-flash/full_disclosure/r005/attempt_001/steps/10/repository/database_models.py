
import json
from typing import Any, Dict, List, Optional, Union

class DocumentRequest:
    """
    Represents a request to the Managed NoSQL Document Store.
    """
    def __init__(self, document_id: str, data: Dict[str, Any]):
        self.document_id = document_id
        self.data = data

    def to_json(self) -> str:
        return json.dumps({"document_id": self.document_id, "data": self.data})

class DocumentResponse:
    """
    Represents a response from the Managed NoSQL Document Store.
    """
    def __init__(self, document_id: str, data: Optional[Dict[str, Any]] = None, success: bool = True, message: Optional[str] = None):
        self.document_id = document_id
        self.data = data
        self.success = success
        self.message = message

    def to_json(self) -> str:
        return json.dumps({
            "document_id": self.document_id,
            "data": self.data,
            "success": self.success,
            "message": self.message
        })

def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a document for storage or retrieval.
    This is a placeholder for actual normalization logic (e.g., schema validation, type conversion).
    """
    # Example normalization: ensure certain fields exist or convert types
    normalized_doc = document.copy()
    if "created_at" not in normalized_doc:
        normalized_doc["created_at"] = None # Or a default timestamp
    return normalized_doc

def denormalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Denormalizes a document after retrieval for application use.
    This is a placeholder for actual denormalization logic.
    """
    # Example denormalization: convert internal IDs to external facing
    denormalized_doc = document.copy()
    return denormalized_doc
