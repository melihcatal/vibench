from typing import Any, Dict

MessagePayload = Dict[str, Any]


class PubSubMessage:
    """Normalization object for Pub/Sub message payloads."""
    def __init__(
        self,
        id: str = None,
        type: str = None,
        payload: MessagePayload = None,
        attributes: Dict[str, str] = None,
    ):
        self.id = id or self._generate_id()
        self.type = type
        self.payload = payload or {}
        self.attributes = attributes or {}

    @staticmethod
    def _generate_id() -> str:
        import uuid
        return str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
            'payload': self.payload,
            'attributes': self.attributes,
        }

    def to_bytes(self) -> bytes:
        """Serialize to JSON bytes."""
        import json
        return json.dumps(self.to_dict()).encode('utf-8')

    @classmethod
    def from_bytes(cls, data: bytes):
        import json
        data_dict = json.loads(data.decode('utf-8'))
        return cls(**data_dict)
