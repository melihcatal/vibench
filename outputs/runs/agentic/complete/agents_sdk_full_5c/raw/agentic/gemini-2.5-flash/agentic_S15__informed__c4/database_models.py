from typing import Dict, Any, Optional

def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a document retrieved from Firestore, e.g., converts Timestamps to strings.
    """
    normalized_doc = document.copy()
    # Example normalization: Convert Firestore Timestamps to ISO format strings
    for key, value in normalized_doc.items():
        if hasattr(value, 'isoformat'): # Check if it's a datetime-like object
            normalized_doc[key] = value.isoformat()
    return normalized_doc

def create_document_payload(data: Dict[str, Any], document_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Creates a standardized payload for upserting documents.
    """
    payload = data.copy()
    if document_id:
        payload["id"] = document_id # For consistency if needed by other systems
    return payload
