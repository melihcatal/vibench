from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

@dataclass
class DocumentRequest:
    collection: str
    document_id: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    query: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DocumentResponse:
    success: bool
    message: str
    data: Optional[Any] = None
    documents: Optional[List[Dict[str, Any]]] = None

def _normalize_document_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes document data before storing it in the NoSQL database.
    This could include:
    - Converting data types
    - Renaming fields
    - Adding/removing metadata
    - Ensuring schema compliance
    """
    # Example: Convert 'createdAt' from datetime object to ISO string if present
    normalized_data = data.copy()
    if 'createdAt' in normalized_data and hasattr(normalized_data['createdAt'], 'isoformat'):
        normalized_data['createdAt'] = normalized_data['createdAt'].isoformat()
    # Add other normalization logic here
    return normalized_data

def _denormalize_document_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Denormalizes document data after retrieving it from the NoSQL database.
    This could include:
    - Converting data types back
    - Reverting field renames
    - Removing internal metadata
    """
    # Example: Convert 'createdAt' from ISO string back to datetime object
    denormalized_data = data.copy()
    if 'createdAt' in denormalized_data and isinstance(denormalized_data['createdAt'], str):
        try:
            from datetime import datetime
            denormalized_data['createdAt'] = datetime.fromisoformat(denormalized_data['createdAt'])
        except ValueError:
            pass # Handle cases where conversion fails or not an ISO string
    # Add other denormalization logic here
    return denormalized_data

def _validate_request_data(request: DocumentRequest) -> bool:
    """
    Validates the incoming DocumentRequest to ensure it meets basic requirements.
    """
    if not request.collection:
        return False, "Collection name is required."
    # Add more specific validation rules based on your data model
    return True, ""
