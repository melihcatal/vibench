class LogEntry:
    def __init__(self, severity, message, component=None):
        self.severity = severity
        self.message = message
        self.component = component

class CorrelatedLogEntry(LogEntry):
    def __init__(self, severity, message, component=None, correlation_id=None):
        super().__init__(severity, message, component)
        self.correlation_id = correlation_id