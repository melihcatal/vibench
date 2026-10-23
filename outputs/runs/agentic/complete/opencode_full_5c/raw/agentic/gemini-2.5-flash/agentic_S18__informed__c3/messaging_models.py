import json
from typing import Any, Dict, List, Optional


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

    def to_json(self) -> bytes:
        return json.dumps(self.data).encode("utf-8")

    @classmethod
    def from_json(
        cls,
        data: bytes,
        message_id: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
    ):
        return cls(json.loads(data.decode("utf-8")), message_id, attributes)


class BatchMessages:
    def __init__(self, messages: List[PubSubMessage]):
        self.messages = messages
