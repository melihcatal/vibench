import json


class PubSubMessage:
    def __init__(self, data: dict, message_id: str = None, attributes: dict = None):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes if attributes is not None else {}

    def to_json(self):
        return json.dumps(self.data)

    @classmethod
    def from_json(
        cls, json_string: str, message_id: str = None, attributes: dict = None
    ):
        return cls(json.loads(json_string), message_id, attributes)


class AuditRecord:
    def __init__(
        self,
        message_id: str,
        status: str,
        timestamp: str,
        payload: dict,
        summary: str = None,
        safety_score: dict = None,
        translated_payload: dict = None,
    ):
        self.message_id = message_id
        self.status = status
        self.timestamp = timestamp
        self.payload = payload
        self.summary = summary
        self.safety_score = safety_score
        self.translated_payload = translated_payload

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "status": self.status,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "summary": self.summary,
            "safety_score": self.safety_score,
            "translated_payload": self.translated_payload,
        }
