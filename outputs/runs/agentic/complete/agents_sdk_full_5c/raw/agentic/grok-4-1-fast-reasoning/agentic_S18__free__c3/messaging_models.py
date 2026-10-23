from dataclasses import dataclass
from typing import Dict, Any
import json

@dataclass
class MessageEvent:
    id: str
    payload: Dict[str, Any]
    attributes: Dict[str, str] = None

def parse_message_data(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode('utf-8'))

def to_message_event(msg) -> MessageEvent:
    payload = parse_message_data(msg.data)
    return MessageEvent(
        id=msg.message_id,
        payload=payload,
        attributes=dict(msg.attributes)
    )