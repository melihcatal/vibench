import json
import logging

# Core provider helper
from observability_client import ManagedLogClient


# Model structures for log payloads
class LogEvent:
    """Local representation of a log event payload.
    "+attributs timestamp, event_name, details, correlation_id"""

    def __init__(
        self, timestamp: int, event_name: str, details: dict, correlation_id: str = None
    ):
        self.timestamp = timestamp
        self.event_name = event_name
        self.details = details
        self.correlation_id = correlation_id

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "event": self.event_name,
            "details": self.details,
            "correlation_id": self.correlation_id,
        }


class LogResponse:
    """Normalization wrapper for responses from managed logging services.
    "+attributs status, data"""

    def __init__(self, status: str, data: dict):
        self.status = status
        self.data = data

    @classmethod
    def from_raw(cls, raw_response: dict):
        # Normalize provider-specific response shape to a common dict
        if raw_response.get("status") == "ok":
            return cls(status="success", data=raw_response.get("payload", {}))
        return cls(status="error", data=raw_response.get("error", {}))
