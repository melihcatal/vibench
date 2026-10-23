class LogEntry:
    def __init__(self, message, timestamp, severity='INFO'):
        self.message = message
        self.timestamp = timestamp
        self.severity = severity

    def to_dict(self):
        return {'message': self.message, 'timestamp': self.timestamp, 'severity': self.severity}