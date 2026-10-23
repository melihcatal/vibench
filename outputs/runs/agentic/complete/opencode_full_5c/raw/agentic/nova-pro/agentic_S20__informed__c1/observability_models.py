class LogEntry:
    def __init__(self, timestamp, severity, message):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message


class LogQuery:
    def __init__(self, filter_, order_by):
        self.filter_ = filter_
        self.order_by = order_by
