class LogEntry:
    def __init__(self, message, correlation_id=None):
        self.message = message
        self.correlation_id = correlation_id