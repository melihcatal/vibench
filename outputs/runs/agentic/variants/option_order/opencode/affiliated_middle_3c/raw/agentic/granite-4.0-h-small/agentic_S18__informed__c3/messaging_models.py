import json
from typing import Dict, Any

# Modeling helpers for Pub/Sub messaging


def create_event(message_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standard event dict with required fields."""
    return {
        "message_id": message_id,
        "payload": payload,
        "timestamp": int(datetime.utcnow().timestamp() * 1000),
    }


# Normalization of response payload to a consistent dict shape


def normalize_response(response: Any) -> Dict[str, Any]:
    if isinstance(response, dict):
        return response
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {}
