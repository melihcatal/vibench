class LogEntry:
    def __init__(self, severity, message, component, operation, correlation_id=None):
        self.severity = severity
        self.message = message
        self.component = component
        self.operation = operation
        self.correlation_id = correlation_id

    def to_dict(self):
        return {
            'severity': self.severity,
            'message': self.message,
            'component': self.component,
            'operation': self.operation,
            'correlation_id': self.correlation_id
        }