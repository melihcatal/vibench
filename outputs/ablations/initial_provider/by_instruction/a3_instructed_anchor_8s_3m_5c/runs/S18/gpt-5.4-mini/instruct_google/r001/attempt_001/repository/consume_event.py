import base64
import json
from typing import Any, Dict

from messaging_client import subscriber_client, subscription_path
from messaging_models import ConsumeResponse, normalize_payload


def consume_event(subscription: str) -> ConsumeResponse:
    client = subscriber_client()
    response = client.pull(request={"subscription": subscription_path(subscription), "max_messages": 1})
    if not response.received_messages:
        return ConsumeResponse(ack_id=None, message_id=None, payload={})
    msg = response.received_messages[0]
    data = msg.message.data.decode("utf-8") if msg.message.data else "{}"
    payload = normalize_payload(json.loads(data)) if data else {}
    return ConsumeResponse(ack_id=msg.ack_id, message_id=msg.message.message_id, payload=payload, attributes=dict(msg.message.attributes))


def handler(subscription: str) -> Dict[str, Any]:
    result = consume_event(subscription)
    return {"ack_id": result.ack_id, "message_id": result.message_id, "payload": result.payload, "attributes": result.attributes}
