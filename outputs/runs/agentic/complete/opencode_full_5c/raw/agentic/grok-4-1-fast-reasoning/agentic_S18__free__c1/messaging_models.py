import json
from typing import Dict, Any


def serialize_event(event: Dict[str, Any]) -> bytes:
    return json.dumps(event).encode("utf-8")


def deserialize_event(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode("utf-8"))


def parse_pubsub_message(pubsub_msg) -> Dict[str, Any]:
    payload = deserialize_event(pubsub_msg.message.data)
    return {
        "payload": payload,
        "message_id": pubsub_msg.message.message_id,
        "attributes": dict(pubsub_msg.message.attributes),
    }
