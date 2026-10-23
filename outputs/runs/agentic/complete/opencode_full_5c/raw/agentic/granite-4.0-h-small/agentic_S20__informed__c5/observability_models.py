from typing import Dict, Any, List


class LogRecord:
    """Normalized log record model."""

    def __init__(
        self, timestamp: str, severity: str, message: str, correlation_id: str = None
    ):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.correlation_id = correlation_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "correlation_id": self.correlation_id,
        }


class LogBatch:
    """Container for a collection of LogRecord objects."""

    def __init__(self, records: List[LogRecord]):
        self.records: List[LogRecord] = records

    def to_dict(self) -> Dict[str, Any]:
        return {"records": [rec.to_dict() for rec in self.records]}
