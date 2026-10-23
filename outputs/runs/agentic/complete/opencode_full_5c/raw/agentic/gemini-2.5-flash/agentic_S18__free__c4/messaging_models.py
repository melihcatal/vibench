import json
from typing import Dict, Any, Optional


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
