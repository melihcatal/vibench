import json
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class PubSubMessage:
    data: Dict[str, Any]
    attributes: Dict[str, str]
    message_id: Optional[str] = None
    ack_id: Optional[str] = None

def encode_event(event: Dict[str, Any]) -> bytes:
    return json.dumps(event, ensure_ascii=False).encode('utf-8')

def decode_data(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode('utf-8'))

def from_pubsub_message(recv_msg) -> PubSubMessage:
    return PubSubMessage(
        data=decode_data(recv_msg.message.data),
        attributes=dict(recv_msg.message.attributes),
        message_id=recv_msg.message.message_id,
        ack_id=recv_msg.ack_id
    )