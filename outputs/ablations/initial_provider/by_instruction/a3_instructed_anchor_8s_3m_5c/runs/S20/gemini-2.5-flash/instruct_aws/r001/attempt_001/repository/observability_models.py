import json
import datetime

class StructuredLogEvent:
    def __init__(self, message: str, severity: str, service: str, correlation_id: str = None, metadata: dict = None):
        self.message = message
        self.severity = severity
        self.service = service
        self.correlation_id = correlation_id
        self.timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.metadata = metadata if metadata is not None else {}

    def to_json(self):
        log_entry = {
            "timestamp": self.timestamp,
            "severity": self.severity,
            "service": self.service,
            "message": self.message,
        }
        if self.correlation_id:
            log_entry["correlation_id"] = self.correlation_id
        log_entry.update(self.metadata)
        return json.dumps(log_entry)
