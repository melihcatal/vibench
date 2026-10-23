from typing import Any, Dict, Optional, TypedDict

class PubSubMessage(TypedDict):
    """Represents a normalized Pub/Sub message structure."""
    data: bytes
    attributes: Dict[str, str]
    message_id: str
    publish_time: str

class EventPayload(TypedDict):
    """Represents a generic event payload structure."""
    event_type: str
    data: Dict[str, Any]
    timestamp: Optional[str]

class PublishRequest(TypedDict):
    """Represents a request to publish a message."""
    topic_id: str
    payload: Dict[str, Any]
    attributes: Optional[Dict[str, str]]
