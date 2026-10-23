class LogPayload:
    def __init__(self, event, timestamp_ms=None):
        self.event = event
        self.timestamp_ms = timestamp_ms or int(time.time() * 1000)


class LogEvent:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message