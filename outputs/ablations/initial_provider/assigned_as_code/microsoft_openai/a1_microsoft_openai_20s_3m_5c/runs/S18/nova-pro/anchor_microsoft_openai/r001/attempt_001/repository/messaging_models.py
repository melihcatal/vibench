import json

class Message:
    def __init__(self, body, attributes=None):
        self.body = body
        self.attributes = attributes or {}

    def to_dict(self):
        return {'Message': self.body, 'MessageAttributes': self.attributes}

    @staticmethod
    def from_dict(data):
        return Message(data['Message'], data.get('MessageAttributes', {}))