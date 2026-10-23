
import dataclasses
from typing import Any, Dict, Optional

@dataclasses.dataclass
class PubSubMessage:
    data: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None
    message_id: Optional[str] = None
    publish_time: Optional[str] = None

@dataclasses.dataclass
class PubSubRequest:
    message: PubSubMessage
    subscription: Optional[str] = None

@dataclasses.dataclass
class PubSubResponse:
    ack_id: str
    message_id: str
    status: str

def normalize_pubsub_request(data: Dict[str, Any]) -> PubSubRequest:
    message_data = data.get("message", {})
    message = PubSubMessage(
        data=message_data.get("data"),
        attributes=message_data.get("attributes"),
        message_id=message_data.get("message_id"),
        publish_time=message_data.get("publish_time"),
    )
    return PubSubRequest(message=message, subscription=data.get("subscription"))
