import json
from typing import Dict, Any, Optional


def serialize_payload(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload).encode("utf-8")


def deserialize_payload(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode("utf-8"))


def pubsub_message_to_dict(received_msg) -> Dict[str, Any]:
    pub_msg = received_msg.message
    payload = deserialize_payload(pub_msg.data)
    return {
        "message_id": pub_msg.message_id,
        "payload": payload,
        "attributes": dict(pub_msg.attributes),
        "ack_id": received_msg.ack_id,
    }
