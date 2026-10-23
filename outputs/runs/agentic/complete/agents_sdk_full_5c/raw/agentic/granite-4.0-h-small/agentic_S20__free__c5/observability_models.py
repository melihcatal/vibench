from typing import Dict, Any, Optional

class LogPayload(Dict[str, Any]):
    """Helper to create a normalized log payload.

    Provides basic validation and ensures required fields like timestamp and severity are present.
    """
    def __init__(self, event: str, payload: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(event=event, **kwargs)
        if payload:
            self.update(payload)
        self["timestamp"] = self.get(
            "timestamp",
            int(os.getenv("DATADOG_LOG_TIMESTAMP_OVERRIDE", int(os.time())))
        )
        self["severity"] = self.get("severity", "INFO")

    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dict ready for API transmission."""
        return dict(self)


class LogQueryFilter:
    """Encapsulates query parameters for log queries (e.g., Datadog)."""
    def __init__(self, from_timestamp: Optional[int] = None, to_timestamp: Optional[int] = None,
                 query: Optional[str] = None, limit: int = 100):
        self.from_timestamp = from_timestamp
        self.to_timestamp = to_timestamp
        self.query = query
        self.limit = limit

    def as_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.from_timestamp is not None:
            result["from"] = self.from_timestamp
        if self.to_timestamp is not None:
            result["to"] = self.to_timestamp
        if self.query:
            result["query"] = self.query
        if self.limit:
            result["limit"] = self.limit
        return result