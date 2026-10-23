from typing import Any, Dict, Optional


class DocumentRequest:
    def __init__(
        self,
        identifier: str,
        payload: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.identifier = identifier
        self.payload = payload
        self.metadata = metadata or {}


class DocumentResponse:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def to_dict(self) -> Dict[str, Any]:
        return self.data


def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Converts raw provider response into a standardized dict format."""
    # Example: strip provider-specific wrappers, rename fields, etc.
    return {
        "id": raw.get("id"),
        "content": raw.get("fields", {}).get("content"),
        "timestamp": raw.get("fields", {}).get("timestamp"),
    }
