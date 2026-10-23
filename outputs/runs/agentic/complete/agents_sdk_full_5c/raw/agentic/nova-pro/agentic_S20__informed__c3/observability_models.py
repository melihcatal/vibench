class LogModel:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message

    def to_dict(self):
        return {'timestamp': self.timestamp, 'message': self.message}