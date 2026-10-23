import json
from typing import Any, Dict


def normalize_request(payload: Any) -> Dict[str, Any]:
    """Convert any Python data structure to a normalized JSON‑serializable dict.
    This helper ensures consistent field names expected by the messaging client.
    """
    if isinstance(payload, dict):
        # Ensure string keys and JSON‑compatible values
        return {str(k): _normalize(v) for k, v in payload.items()}
    # Fallback: wrap scalar values in a dict under a key like "message"
    return {"message": str(payload)}


def _normalize(value: Any) -> Any:
    """Recursively handle lists, dicts, and basic types for JSON serialization."""
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    # Convert other truthy/falsy types to strings (or keep numbers, booleans)
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def parse_response(raw_body: bytes) -> Any:
    """Parse a raw response body (bytes) into a Python object.
    Most messaging services return JSON, so a JSON decode is attempted.
    """
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        # Return raw bytes if not JSON‑compatible (e.g., a binary payload)
        return raw_body
