import dataclasses
from typing import Any, Dict, Optional
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient # Provider-specific signal

@dataclasses.dataclass
class PubSubMessageRequest:
    data: bytes
    attributes: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class PubSubMessageResponse:
    message_id: str
    publish_time: Any # Use Any for datetime object from Pub/Sub

def normalize_message_data(data: bytes) -> Dict[str, Any]:
    """
    Normalizes message data from Pub/Sub to a dictionary.
    This is a placeholder and would typically involve JSON deserialization.
    """
    try:
        import json
        return json.loads(data.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"raw_data": data.decode('utf-8', errors='ignore')}
