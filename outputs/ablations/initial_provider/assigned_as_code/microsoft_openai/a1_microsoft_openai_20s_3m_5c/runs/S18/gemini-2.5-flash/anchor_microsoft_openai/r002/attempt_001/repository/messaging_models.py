import json

class PubSubMessage:
    def __init__(self, message_id, content_type, body, attributes=None):
        self.message_id = message_id
        self.content_type = content_type
        self.body = body
        self.attributes = attributes if attributes is not None else {}

    def to_json(self):
        return {
            "message_id": self.message_id,
            "content_type": self.content_type,
            "body": self.body,
            "attributes": self.attributes
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get("message_id"),
            json_data.get("content_type"),
            json_data.get("body"),
            json_data.get("attributes")
        )
