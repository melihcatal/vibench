from typing import Dict, Any

class Message:
    def __init__(self, body: str, message_id: str, content_type: str, properties: Dict[str, Any] = None):
        self.body = body
        self.message_id = message_id
        self.content_type = content_type
        self.properties = properties or {}

class PublishRequest:
    def __init__(self, event: Dict[str, Any], attributes: Dict[str, str] = None):
        self.event = event
        self.attributes = attributes or {}

class PublishResponse:
    def __init__(self, message_id: str):
        self.message_id = message_id

class ConsumeResponse:
    def __init__(self, message_id: str, body: str, properties: Dict[str, Any]):
        self.message_id = message_id
        self.body = body
        self.properties = properties

class BatchPublishRequest:
    def __init__(self, events: list[Dict[str, Any]]):
        self.events = events

class BatchPublishResponse:
    def __init__(self, message_ids: list[str]):
        self.message_ids = message_ids
