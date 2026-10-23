import json
from typing import Any, Dict


def normalize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure all document fields are JSON-serializable.
    Convert non-serializable types (e.g., datetime) to strings.
    """
    normalized = {}
    for key, value in doc.items():
        if hasattr(value, "isoformat"):
            # e.g., datetime.datetime
            normalized[key] = value.isoformat()
        elif isinstance(value, (list, dict, str, int, float, bool, type(None))):
            normalized[key] = value
        else:
            normalized[key] = str(value)
    return normalized


def denormalize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Placeholder for future denormalization (e.g., parsing ISO strings back to datetime).
    Currently returns the dict unchanged.
    """
    return doc
