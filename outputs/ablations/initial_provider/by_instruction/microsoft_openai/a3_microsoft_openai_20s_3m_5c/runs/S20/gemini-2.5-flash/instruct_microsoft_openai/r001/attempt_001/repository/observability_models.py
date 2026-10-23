import json
from typing import Dict, Any, Optional

class LogEvent:
    def __init__(self, message: str, level: str = "info", timestamp: Optional[str] = None, **kwargs):
        self.message = message
        self.level = level
        self.timestamp = timestamp
        self.properties = kwargs

    def to_json(self) -> str:
        data = {
            "message": self.message,
            "level": self.level,
            "timestamp": self.timestamp,
            "properties": self.properties
        }
        return json.dumps(data)

class StructuredLogEvent(LogEvent):
    def __init__(self, message: str, level: str = "info", timestamp: Optional[str] = None, **kwargs):
        super().__init__(message, level, timestamp, **kwargs)

class CorrelatedLogEvent(LogEvent):
    def __init__(self, message: str, correlation_id: str, level: str = "info", timestamp: Optional[str] = None, **kwargs):
        super().__init__(message, level, timestamp, correlation_id=correlation_id, **kwargs)
        self.correlation_id = correlation_id
