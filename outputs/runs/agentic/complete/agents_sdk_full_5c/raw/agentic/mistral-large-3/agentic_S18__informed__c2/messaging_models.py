"""Local request, response, and normalization helpers for Pub/Sub Messaging."""
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List


@dataclass
class Message:
    """Normalized message structure for Pub/Sub messaging."""
    message_id: str
    body: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None
    publish_time: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to a dictionary for serialization."""
        return asdict(self)


@dataclass
class BatchMessage:
    """Normalized batch message structure for Pub/Sub messaging."""
    messages: List[Message]
    topic: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert batch messages to a dictionary for serialization."""
        return {
            "topic": self.topic,
            "messages": [msg.to_dict() for msg in self.messages]
        }


def normalize_pubsub_message(raw_message: Any) -> Message:
    """Normalize Google Cloud Pub/Sub message to local Message model."""
    return Message(
        message_id=raw_message.message_id,
        body=raw_message.data.decode("utf-8"),
        attributes=raw_message.attributes,
        publish_time=raw_message.publish_time
    )


def normalize_service_bus_message(raw_message: Any) -> Message:
    """Normalize Azure Service Bus message to local Message model."""
    return Message(
        message_id=raw_message.message_id,
        body=raw_message.body,
        attributes={
            "content_type": raw_message.content_type,
            "label": raw_message.label
        }
    )