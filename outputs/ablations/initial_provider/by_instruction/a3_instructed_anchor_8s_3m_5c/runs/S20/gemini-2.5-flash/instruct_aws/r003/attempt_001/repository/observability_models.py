import json
from typing import Dict, Any, Optional

class LogEvent:
    def __init__(self, message: str, severity: str, timestamp: int, metadata: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.metadata = metadata if metadata is not None else {}

    def to_json_string(self) -> str:
        event_data = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }
        return json.dumps(event_data)
