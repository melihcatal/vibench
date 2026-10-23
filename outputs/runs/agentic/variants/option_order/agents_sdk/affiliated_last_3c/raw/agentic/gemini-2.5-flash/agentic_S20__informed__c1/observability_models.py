from typing import Optional, Dict, Any
from datetime import datetime

class LogEntry:
    def __init__(self, timestamp: str, severity: str, message: str,
                 component: Optional[str] = None, request_id: Optional[str] = None,
                 full_payload: Optional[Dict[str, Any]] = None):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.component = component
        self.request_id = request_id
        self.full_payload = full_payload

    @classmethod
    def from_gcp_log_entry(cls, gcp_entry: Any): # gcp_entry is google.cloud.logging.LogEntry
        message = ""
        component = None
        request_id = None
        if isinstance(gcp_entry.payload, dict):
            message = gcp_entry.payload.get("message", str(gcp_entry.payload))
            component = gcp_entry.payload.get("component")
            request_id = gcp_entry.payload.get("request_id")
        elif isinstance(gcp_entry.payload, str):
            message = gcp_entry.payload
        else:
            message = str(gcp_entry.payload)

        return cls(
            timestamp=gcp_entry.timestamp.isoformat(),
            severity=gcp_entry.severity,
            message=message,
            component=component,
            request_id=request_id,
            full_payload=gcp_entry.to_api_repr()
        )

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "message": self.message,
            "component": self.component,
            "request_id": self.request_id,
            "full_payload": self.full_payload
        }

class LogQueryResult:
    def __init__(self, entries: list[LogEntry], total_results: int):
        self.entries = entries
        self.total_results = total_results

    def to_dict(self):
        return {
            "entries": [entry.to_dict() for entry in self.entries],
            "total_results": self.total_results
        }

if __name__ == "__main__":
    # Example usage (without actual GCP LogEntry object)
    print("Observability models defined.")
    # Simulate a GCP LogEntry for demonstration
    class MockGCPLogEntry:
        def __init__(self, payload, severity, timestamp):
            self.payload = payload
            self.severity = severity
            self.timestamp = timestamp
        def to_api_repr(self):
            return {"jsonPayload": self.payload, "severity": self.severity, "timestamp": self.timestamp.isoformat()}

    mock_entry_payload = {"message": "Test log message", "component": "test-component", "request_id": "123"}
    mock_gcp_entry = MockGCPLogEntry(mock_entry_payload, "INFO", datetime.utcnow())

    log_entry_model = LogEntry.from_gcp_log_entry(mock_gcp_entry)
    print(f"Parsed LogEntry: {log_entry_model.to_dict()}")

    query_results = LogQueryResult(entries=[log_entry_model], total_results=1)
    print(f"LogQueryResult: {query_results.to_dict()}")
