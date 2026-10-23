import json

class MessagePayload:
    def __init__(self, event_id, event_type, data):
        self.event_id = event_id
        self.event_type = event_type
        self.data = data

    def to_json(self):
        return json.dumps({
            "event_id": self.event_id,
            "event_type": self.event_type,
            "data": self.data
        })

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        return cls(data["event_id"], data["event_type"], data["data"])

class PublishResponse:
    def __init__(self, message_id):
        self.message_id = message_id

class ConsumeResponse:
    def __init__(self, message_id, receipt_handle, payload):
        self.message_id = message_id
        self.receipt_handle = receipt_handle
        self.payload = payload
