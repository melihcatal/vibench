class LogEvent:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message

    @classmethod
    def from_dict(cls, log_event_dict):
        return cls(
            timestamp=log_event_dict["timestamp"], message=log_event_dict["message"]
        )
