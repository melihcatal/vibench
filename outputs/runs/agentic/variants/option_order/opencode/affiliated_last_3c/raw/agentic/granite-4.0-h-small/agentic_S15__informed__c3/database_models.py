from typing import Any, Dict, List, Optional


# Generic request envelope for document operations
class DocumentRequest(Dict[str, Any]):
    def __init__(self, payload: dict, metadata: Optional[dict] = None):
        self.payload = payload  # required data for upsert / update
        self.metadata = metadata or {
            "created_at": None,
            "updated_at": None,
        }

    def to_dict(self) -> dict:
        return {
            "payload": self.payload,
            "metadata": self.metadata,
        }


# Normalized response envelope
class DocumentResponse(Dict[str, Any]):
    def __init__(self, data: dict, status: str = "ok"):
        self.data = data  # actual document fields
        self.status = status  # ok / error / validation-failed
        self.errors: Optional[Dict[str, List[str]]] = None

    def to_dict(self) -> dict:
        base = {"data": self.data, "status": self.status}
        if self.errors:
            base["errors"] = self.errors
        return base


# Helper utilities for schema validation / normalization
def normalize_insert(payload: dict) -> Dict[str, Any]:
    """Basic type‑casting and required‑field validation for new documents."""
    # Example: ensure `_id` exists and is a string
    if "_id" not in payload or not isinstance(payload["_id"], str):
        raise ValueError("_id field missing or not a string")
    # Convert timestamps if present
    for key in ("created_at", "updated_at"):
        if key in payload and isinstance(payload[key], str):
            # Expect ISO‑8601; you can parse to datetime here if needed
            payload[key] = payload[key]
    return payload


def normalize_update(payload: dict) -> Dict[str, Any]:
    """Validate fields that can be updated, ensure idempotency."""
    if "_id" not in payload:
        raise ValueError("_id must be present for updates")
    # Optional version check for conditional update logic
    if "version" in payload and not isinstance(payload["version"], int):
        raise ValueError("version must be an integer")
    return payload


# -------------------------------------------------------------------
# Public helpers exposed to other modules
# -------------------------------------------------------------------


def coerce_primitive(value: Any) -> Any:
    """Coerce a value to a JSON‑serializable primitive when needed."""
    if isinstance(value, (dict, list)):
        # Recursively ensure nested structures are serializable
        return (
            {k: coerce_primitive(v) for k, v in value.items()}
            if isinstance(value, dict)
            else [coerce_primitive(v) for v in value]
        )
    return value


def serialize_object(obj: Any) -> Dict[str, Any]:
    """Serialize an object into a plain dict for storage.","""
    return (
        {k: coerce_primitive(v) for k, v in vars(obj).items()}
        if hasattr(obj, "__dict__")
        else obj
    )
