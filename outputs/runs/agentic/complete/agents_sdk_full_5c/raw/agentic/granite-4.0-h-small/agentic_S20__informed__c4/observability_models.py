import json
from typing import Any

class LogEvent:
    """Helper class to standardize log payloads sent to observability services.

    Attributes:
        timestamp: Unix epoch seconds or None (service will fill)
        message: Text of the log
        event_type: Semantic tag for the log (e.g., 'request_start')
        level: Severity (info, warn, error, debug)
        request_id: Correlation ID linking related logs
        metadata: Arbitrary key‑value pairs to enrich the event
    """
    def __init__(self, *, message: str, event_type: Optional[str] = None,
                 level: str = 'info', request_id: Optional[str] = None,
                 timestamp: Optional[int] = None, metadata: Optional[dict] = None):
        self.timestamp = timestamp
        self.message = message
        self.event_type = event_type
        self.level = level
        self.request_id = request_id
        self.metadata = metadata or {}

    def to_dict(self) -> dict:
        """Serialize to a JSON‑serializable dict suitable for Datadog or other APIs.
        """
        payload: dict = {
            'timestamp': self.timestamp,
            'message': self.message,
            'level': self.level
        }
        if self.event_type:
            payload['event_type'] = self.event_type
        if self.request_id:
            payload['request_id'] = self.request_id
        if self.metadata:
            payload['metadata'] = self.metadata
        return payload
