class LogEntry:
    def __init__(self, payload):
        self.payload = payload

    def to_struct(self):
        return {'jsonPayload': self.payload}