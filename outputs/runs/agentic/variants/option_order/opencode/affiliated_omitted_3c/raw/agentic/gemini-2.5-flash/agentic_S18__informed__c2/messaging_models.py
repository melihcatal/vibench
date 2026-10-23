import json
from typing import Dict, Any


class EventMessage:
    def __init__(
        self,
        message_id: str,
        payload: Dict[str, Any],
        attributes: Dict[str, Any] = None,
    ):
        self.message_id = message_id
        self.payload = payload
        self.attributes = attributes if attributes is not None else {}

    def to_json_string(self) -> str:
        return json.dumps(
            {
                "message_id": self.message_id,
                "payload": self.payload,
                "attributes": self.attributes,
            }
        )

    @classmethod
    def from_json_string(cls, json_string: str):
        data = json.loads(json_string)
        return cls(
            message_id=data["message_id"],
            payload=data["payload"],
            attributes=data.get("attributes", {}),
        )
