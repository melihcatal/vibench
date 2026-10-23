class Event:
    def __init__(self, event_id, payload):
        self.event_id = event_id
        self.payload = payload

class Message:
    def __init__(self, message_id, content_type, body):
        self.message_id = message_id
        self.content_type = content_type
        self.body = body