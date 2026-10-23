import os


class DocumentRequest:
    """Payload builder for upserting/fetching documents."""

    def __init__(self, identifier: str, payload: dict):
        self.identifier = identifier
        self.payload = payload


class DocumentResponse:
    """Normalized response for fetched documents."""

    def __init__(self, raw: dict):
        self.raw = raw
        # Example normalization: ensure fields are present
        self.id = raw.get("id")
        self.version = raw.get("version")
        # Add more field mappings as needed


class QueryOptions:
    """Options for scanning / filtering queries."""

    def __init__(self, field: str, value):
        self.field = field
        self.value = value


class ConditionalUpdate:
    """Data structure for version‑aware conditional updates."""

    def __init__(self, identifier: str, fields: dict, condition: dict):
        self.identifier = identifier
        self.fields = fields
        self.condition = condition  # e.g., {"version": 3}


# Provider‑agnostic utility functions (can be extended later)
async def safe_fetch(client, identifier):
    """Fetch a document safely, returning None if missing."""
    try:
        return client.get(identifier)
    except Exception:
        return None
