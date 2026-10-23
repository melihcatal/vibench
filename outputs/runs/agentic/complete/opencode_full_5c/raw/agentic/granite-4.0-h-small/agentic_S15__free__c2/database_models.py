import json
from typing import Dict, Any


class DocumentRequest:
    """Helper to construct requests for the DocumentDB client."""

    def __init__(self, doc_id: str, data: Dict[str, Any]):
        self.doc_id = doc_id
        self.data = data
        self.normalized = self._normalize(data)

    def _normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Convert snake_case keys to camelCase expected by DocumentDB
        normalized = {}
        for k, v in data.items():
            camel = "".join(word.capitalize() or "_" for word in k.split("_"))
            normalized[camel] = v
        return normalized

    def to_payload(self) -> Dict[str, Any]:
        return self.normalized


class DocumentResponse:
    """Response wrapper for fetched or updated documents."""

    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.normalized = self._denormalize(raw)

    def _denormalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Convert camelCase back to snake_case for internal use
        normalized = {}
        for k, v in data.items():
            parts = []
            for i, char in enumerate(k):
                if i > 0 and char.isupper():
                    parts.append("_")
                parts.append(char.lower())
            snake = "".join(parts)
            normalized[snake] = v
        return normalized

    def to_dict(self) -> Dict[str, Any]:
        return self.normalized
