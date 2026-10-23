import json
from typing import Dict, Any


def normalize_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Convert SDK‑compatible model objects to plain JSON dictionaries.

    Example: client expects field names in snake_case while caller may use camelCase.
    """
    normalized = {}
    for k, v in payload.items():
        # Simple snake_case conversion for demonstration
        new_k = "".join(["_" + c.lower() if c.isupper() else c for c in k]).lstrip("_")
        normalized[new_k] = v
    return normalized


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Post‑process a provider response to a consistent internal format.

    Removes provider‑specific metadata and returns only the document body.
    """
    # Example: response may contain '_id', '_rev', 'result', etc.
    if isinstance(response, dict):
        return response.get("result") or response
    return response
