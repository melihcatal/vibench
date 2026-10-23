from typing import Dict, Any


class SecretRequest:
    """Normalization model for secret fetch requests."""

    def __init__(self, name: str, version: Any = None):
        self.name = name
        self.version = version  # version or staged label

    def as_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "version": self.version}


class SecretResponse:
    """Response wrapper with parsed secret content."""

    def __init__(self, raw: str):
        self.raw = raw
        self.parsed: Any = None
        try:
            self.parsed = json.loads(raw)
        except json.JSONDecodeError:
            self.parsed = raw  # fallback to raw string


class SecretInfo:
    """Utility class to hold metadata about a secret."""

    def __init__(self, name: str, version: Any, fetched_at: str):
        self.name = name
        self.version = version
        self.fetched_at = fetched_at
