
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class PubSubMessage:
    """Represents a message to be published or consumed."""
    data: bytes
    attributes: Optional[Dict[str, str]] = field(default_factory=dict)
    message_id: Optional[str] = None

@dataclass
class PublishRequest:
    """Represents a request to publish one or more messages."""
    messages: list[PubSubMessage]
    topic: str

@dataclass
class PublishResponse:
    """Represents a response from a publish operation."""
    message_ids: list[str]

@dataclass
class ConsumeResponse:
    """Represents a response from a consume operation."""
    message: Optional[PubSubMessage]
    ack_id: Optional[str] = None

class MessageNormalizer:
    """Provides utility methods for normalizing message data."""
    @staticmethod
    def to_json_bytes(payload: Dict[str, Any]) -> bytes:
        """Converts a dictionary payload to JSON bytes."""
        import json
        return json.dumps(payload).encode('utf-8')

    @staticmethod
    def from_json_bytes(data: bytes) -> Dict[str, Any]:
        """Converts JSON bytes to a dictionary payload."""
        import json
        return json.loads(data.decode('utf-8'))
