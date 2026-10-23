import json
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MessageEvent:
    message_id: str
    data: Dict[str, Any]
    attributes: Optional[Dict[str, str]] = None

def normalize_message(pubsub_message) -&gt; MessageEvent:
    data = json.loads(pubsub_message.data.decode('utf-8'))
    attributes = dict(pubsub_message.attributes) if pubsub_message.attributes else {}
    return MessageEvent(
        message_id=pubsub_message.message_id,
        data=data,
        attributes=attributes
    )