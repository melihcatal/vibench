import json
from typing import Dict, Any, List, Optional


class PubSubMessage:
    def __init__(
        self,
        data: Dict[str, Any],
        message_id: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ):
        self.data = data
        self.message_id = message_id
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> str:
        return json.dumps(self.data)

    @classmethod
    def from_json(
        cls,
        json_str: str,
        message_id: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ):
        return cls(json.loads(json_str), message_id, attributes)


class BatchPubSubMessage:
    def __init__(self, messages: List[PubSubMessage]):
        self.messages = messages


class MessageProcessingResult:
    def __init__(
        self,
        message_id: str,
        status: str,
        summary: Optional[str] = None,
        safety_score: Optional[Dict[str, Any]] = None,
        translated_text: Optional[str] = None,
        audit_id: Optional[str] = None,
    ):
        self.message_id = message_id
        self.status = status
        self.summary = summary
        self.safety_score = safety_score
        self.translated_text = translated_text
        self.audit_id = audit_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "status": self.status,
            "summary": self.summary,
            "safety_score": self.safety_score,
            "translated_text": self.translated_text,
            "audit_id": self.audit_id,
        }
