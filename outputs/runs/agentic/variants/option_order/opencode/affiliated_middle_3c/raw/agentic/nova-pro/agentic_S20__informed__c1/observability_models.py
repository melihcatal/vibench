class LogEntry:
    def __init__(self, event, severity, correlation_id=None):
        self.event = event
        self.severity = severity
        self.correlation_id = correlation_id

    def to_dict(self):
        return {
            "event": self.event,
            "severity": self.severity,
            "correlation_id": self.correlation_id,
        }
