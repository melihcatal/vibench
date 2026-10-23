import json


def embed_secret_audit(note: str, secret_id: str = None) -> str:
    """Create a JSON payload that can be used for semantic searching of audit notes.
    When secret_id is supplied, it becomes part of the indexed data for linking back to the secret."""
    payload = {
        "timestamp": __timestamp__(),
        "note": note,
    }
    if secret_id:
        payload["secret_id"] = secret_id
    # Return a compact JSON string (whitespace is fine, includes newlines for readability)
    return json.dumps(payload, indent=2)


# Simple UTC timestamp helper
from datetime import datetime


def __timestamp__() -> str:
    return datetime.utcnow().isoformat() + "Z"
