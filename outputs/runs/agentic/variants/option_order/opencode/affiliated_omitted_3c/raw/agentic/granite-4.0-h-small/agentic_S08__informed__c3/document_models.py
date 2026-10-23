import json
import os


class DocumentRequest:
    """Container for a raw document payload to be sent to the extraction service."""

    def __init__(self, file_bytes: bytes):
        self.file_bytes = file_bytes
        self.content_type = (
            "application/pdf" if file_bytes else "application/octet-stream"
        )

    def to_dict(self) -> dict:
        """Return a dict suitable for JSON serialization when needed."""
        return {"bytes": self.file_bytes, "content_type": self.content_type}

    def to_file(self, path: str) -> None:
        """Persist the raw bytes locally (useful for debugging)."""
        with open(path, "wb") as f:
            f.write(self.file_bytes)


class DocumentResponse:
    """Container for a raw response received from an extraction service."""

    def __init__(self, raw_response: dict):
        self.raw = raw_response
        # Lazy decoded JSON (if the service returns JSON string)
        self.json_data = None
        try:
            self.json_data = json.loads(raw_response.get("Body", ""))
        except (TypeError, json.JSONDecodeError):
            self.json_data = {}

    def get_field(self, key: str, default=None) -> any:
        """Convenient access to nested fields."""
        return self.json_data.get(key, default)

    def as_json(self) -> str:
        """Return the raw JSON string (if available)."""
        return json.dumps(self.json_data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Provider‑agnostic helpers for request building & response parsing
# ---------------------------------------------------------------------------


def build_standard_request(file_bytes: bytes) -> DocumentRequest:
    """Create a DocumentRequest for the currently configured provider."""
    return DocumentRequest(file_bytes)


def parse_standard_response(raw: dict) -> DocumentResponse:
    """Create a DocumentResponse from a raw SDK/REST payload."""
    return DocumentResponse(raw)
