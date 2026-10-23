class LogEntry:
    def __init__(self, severity, message, correlation_id=None):
        self.severity = severity
        self.message = message
        self.correlation_id = correlation_id

    def to_dict(self):
        return {
            'severity': self.severity,
            'message': self.message,
            'correlationId': self.correlation_id
        }
