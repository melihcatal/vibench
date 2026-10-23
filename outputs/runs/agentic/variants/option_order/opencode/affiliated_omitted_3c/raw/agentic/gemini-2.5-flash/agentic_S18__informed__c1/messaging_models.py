import json
from typing import Any, Dict


class EventMessage:
    """
    A simple model for a generic event message.
    """

    def __init__(
        self,
        message_id: str,
        payload: Dict[str, Any],
        attributes: Dict[str, str] = None,
    ):
        self.message_id = message_id
        self.payload = payload
        self.attributes = attributes if attributes is not None else {}

    def to_json(self) -> str:
        return json.dumps(
            {
                "message_id": self.message_id,
                "payload": self.payload,
                "attributes": self.attributes,
            }
        )

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls(data["message_id"], data["payload"], data.get("attributes"))


class PublishResponse:
    """
    Normalizes a publish operation response.
    """

    def __init__(self, message_id: str = None, success: bool = True, error: str = None):
        self.message_id = message_id
        self.success = success
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "success": self.success,
            "error": self.error,
        }
