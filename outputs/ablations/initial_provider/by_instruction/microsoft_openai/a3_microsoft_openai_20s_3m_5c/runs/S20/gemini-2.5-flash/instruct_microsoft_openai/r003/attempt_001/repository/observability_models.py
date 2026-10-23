import json
from typing import Dict, Any, List

class StructuredLogEvent:
    def __init__(self, message: str, severity: str, timestamp: str, **kwargs):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.properties = kwargs

    def to_json(self) -> str:
        data = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
            **self.properties
        }
        return json.dumps(data)

class CorrelatedLogEvent:
    def __init__(self, message: str, correlation_id: str, service_name: str, timestamp: str, **kwargs):
        self.message = message
        self.correlation_id = correlation_id
        self.service_name = service_name
        self.timestamp = timestamp
        self.properties = kwargs

    def to_json(self) -> str:
        data = {
            "message": self.message,
            "correlation_id": self.correlation_id,
            "service_name": self.service_name,
            "timestamp": self.timestamp,
            **self.properties
        }
        return json.dumps(data)

class LogQueryResult:
    def __init__(self, logs: List[Dict[str, Any]]):
        self.logs = logs

    def to_json(self) -> str:
        return json.dumps(self.logs)
