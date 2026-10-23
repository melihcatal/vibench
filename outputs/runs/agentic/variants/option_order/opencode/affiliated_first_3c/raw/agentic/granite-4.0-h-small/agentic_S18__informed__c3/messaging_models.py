import json
from typing import Any, Dict, Optional


def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure required fields are present and convert to JSON‑serializable format."""
    ev = dict(event)  # shallow copy
    # required fields
    if "id" not in ev:
        ev["id"] = str(uuid.uuid4())
    if "timestamp" not in ev:
        ev["timestamp"] = int(time.time())
    return ev


def parse_response(resp_body: bytes) -> Optional[Dict[str, Any]]:
    """Decode a JSON response, return None on empty payload."""
    if not resp_body:
        return None
    try:
        return json.loads(resp_body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response")


# Utilities for dead-letter handling


def enrich_with_dl_metadata(
    original_topic: str, original_key: Optional[str], payload: Dict[str, Any]
) -> Dict[str, Any]:
    """Add dead‑letter metadata to a payload."""
    return {
        "metadata": {
            "original_topic": original_topic,
            "original_key": original_key,
            "delivery_attempt": 1,
        },
        "payload": payload,
    }
