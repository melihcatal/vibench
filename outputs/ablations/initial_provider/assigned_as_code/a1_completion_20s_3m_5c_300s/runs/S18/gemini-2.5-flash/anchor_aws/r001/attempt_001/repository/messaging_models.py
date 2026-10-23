from typing import Dict, Any

class Message:
    def __init__(self, id: str, body: Dict[str, Any], attributes: Dict[str, str] = None):
        self.id = id
        self.body = body
        self.attributes = attributes if attributes is not None else {}

    def to_dict(self):
        return {
            "id": self.id,
            "body": self.body,
            "attributes": self.attributes
        }

class PublishRequest:
    def __init__(self, event_data: Dict[str, Any], message_attributes: Dict[str, Any] = None):
        self.event_data = event_data
        self.message_attributes = message_attributes if message_attributes is not None else {}

class PublishResponse:
    def __init__(self, message_id: str):
        self.message_id = message_id

class ConsumeResponse:
    def __init__(self, messages: list[Message]):
        self.messages = messages
