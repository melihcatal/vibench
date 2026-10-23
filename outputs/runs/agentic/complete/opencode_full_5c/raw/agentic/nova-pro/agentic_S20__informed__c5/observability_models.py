class LogEntry:
    def __init__(self, message, severity, timestamp):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
