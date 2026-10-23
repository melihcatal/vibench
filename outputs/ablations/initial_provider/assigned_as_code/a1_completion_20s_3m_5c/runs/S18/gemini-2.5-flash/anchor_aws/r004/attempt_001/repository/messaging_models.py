import json

class MessagePayload:
    def __init__(self, event_data: dict):
        self.event_data = event_data

    def to_json(self):
        return json.dumps(self.event_data)

    @classmethod
    def from_json(cls, json_string: str):
        return cls(json.loads(json_string))

class MessageResponse:
    def __init__(self, message_id: str, status: str = "SUCCESS", details: dict = None):
        self.message_id = message_id
        self.status = status
        self.details = details or {}

    def to_dict(self):
        return {"message_id": self.message_id, "status": self.status, "details": self.details}
