class LogEntry:
    def __init__(self, correlation_id, event_type, timestamp, **kwargs):
        self.correlation_id = correlation_id
        self.event_type = event_type
        self.timestamp = timestamp
        self.__dict__.update(kwargs)

    def to_dict(self):
        return self.__dict__