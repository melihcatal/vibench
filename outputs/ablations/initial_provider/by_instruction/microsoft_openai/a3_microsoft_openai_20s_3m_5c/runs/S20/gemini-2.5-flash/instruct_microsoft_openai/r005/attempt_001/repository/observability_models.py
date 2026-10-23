from typing import Dict, Any, List

class StructuredLogEvent:
    def __init__(self, message: str, severity: str, service_name: str, **kwargs):
        self.message = message
        self.severity = severity
        self.service_name = service_name
        self.data = kwargs

    def to_json(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "severity": self.severity,
            "service_name": self.service_name,
            **self.data
        }

class CorrelatedLogEvent(StructuredLogEvent):
    def __init__(self, message: str, severity: str, service_name: str, correlation_id: str, **kwargs):
        super().__init__(message, severity, service_name, **kwargs)
        self.correlation_id = correlation_id

    def to_json(self) -> Dict[str, Any]:
        base_json = super().to_json()
        base_json["correlation_id"] = self.correlation_id
        return base_json

class LogQueryResult:
    def __init__(self, raw_data: List[Dict[str, Any]]):
        self.raw_data = raw_data

    def get_first_message(self) -> str:
        if self.raw_data and "message" in self.raw_data[0]:
            return self.raw_data[0]["message"]
        return ""