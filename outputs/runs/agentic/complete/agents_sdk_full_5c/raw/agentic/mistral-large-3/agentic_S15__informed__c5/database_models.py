from typing import Dict, Any
from datetime import datetime

def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a document for storage in Azure Cosmos DB.
    Ensures required fields and consistent types.
    """
    normalized = document.copy()
    
    # Ensure system fields are present
    if 'createdAt' not in normalized:
        normalized['createdAt'] = datetime.utcnow().isoformat()
    
    if 'updatedAt' not in normalized:
        normalized['updatedAt'] = datetime.utcnow().isoformat()
    
    # Ensure all values are JSON-serializable
    for key, value in normalized.items():
        if isinstance(value, datetime):
            normalized[key] = value.isoformat()
    
    return normalized