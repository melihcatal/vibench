import json
from typing import Any, Dict, Optional

# Local request/response and normalization helpers


class DocumentRequest:
    """Encapsulates a request payload for a managed NoSQL operation.
    Attributes:
        primary_id: The unique identifier of the document.
        fields: Optional dict of fields to set or query.
        filter: Optional criteria to filter/query documents.
    """

    def __init__(
        self,
        primary_id: str,
        fields: Optional[Dict[str, Any]] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.primary_id = primary_id
        self.fields = fields or {}
        self.filter = filter or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the request to a dict suitable for the concrete provider."""
        payload = {"id": self.primary_id}
        if self.fields:
            payload["fields"] = self.fields
        if self.filter:
            payload["filter"] = self.filter
        return payload


class DocumentResponse:
    """Encapsulates a response payload from a managed NoSQL operation.
    Common attributes are normalized to a consistent shape.
    """

    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.document = self._extract_document(raw)

    def _extract_document(self, raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Adapter to pull a document out of the raw provider response.
        Override per concrete provider if the shape differs.
        """
        # Default assumes the document is under a top‑level ‘document’ key.
        return raw.get("document")

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON‑serializable representation."""
        return {"document": self.document}


def normalize_field_names(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize field names for cross‑provider consistency.
    Example: convert camelCase to snake_case if required by the target service.
    """
    result = {}
    for k, v in data.items():
        # Simple conversion; extend with deeper recursion if needed.
        snake = "".join(["_" + c.lower() if c.isupper() else c for c in k]).lstrip("_")
        result[snake] = v
    return result


# Helper to load configuration from environment (used by database_client.py)

import os


def get_env_or_raise(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value
