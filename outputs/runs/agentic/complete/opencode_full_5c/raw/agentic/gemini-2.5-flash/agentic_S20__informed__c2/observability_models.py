import json
from datetime import datetime


class StructuredLog:
    def __init__(self, message: str, severity: str, component: str, data: dict = None):
        self.message = message
        self.severity = severity
        self.component = component
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.data = data if data is not None else {}

    def to_json(self):
        return {
            "message": self.message,
            "severity": self.severity,
            "component": self.component,
            "timestamp": self.timestamp,
            "data": self.data,
        }


class CorrelatedLog:
    def __init__(
        self, message: str, correlation_id: str, step: str, severity: str = "INFO"
    ):
        self.message = message
        self.correlation_id = correlation_id
        self.step = step
        self.severity = severity
        self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_json(self):
        return {
            "message": self.message,
            "correlation_id": self.correlation_id,
            "step": self.step,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
