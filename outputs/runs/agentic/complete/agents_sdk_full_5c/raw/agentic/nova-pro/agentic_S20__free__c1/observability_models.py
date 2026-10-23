class LogEntry:
    def __init__(self, timestamp, level, message, correlation_id=None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.correlation_id = correlation_id