from typing import Dict, Any, List, Optional
from datetime import datetime

class LogEntry:
    def __init__(self, message: str, severity: str, timestamp: datetime, properties: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.properties = properties if properties is not None else {}
        self.correlation_id = correlation_id

    def to_json(self) -> Dict[str, Any]:
        data = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.properties:
            data["properties"] = self.properties
        if self.correlation_id:
            data["correlation_id"] = self.correlation_id
        return data

class LogQueryResult:
    def __init__(self, entries: List[LogEntry], query_time: datetime, total_count: int):
        self.entries = entries
        self.query_time = query_time
        self.total_count = total_count
