import json

from messaging_client import subscriber_client, subscription_path
from messaging_models import ConsumeResponse, normalize_payload


def consume_event(subscription: str):
    client = subscriber_client()
    response = client.pull(
        subscription=subscription_path(subscription), max_messages=1, timeout=10
    )
    if not response.received_messages:
        return None
    msg = response.received_messages[0]
    payload = json.loads(msg.message.data.decode("utf-8")) if msg.message.data else {}
    item = ConsumeResponse(
        message_id=msg.message.message_id,
        payload=normalize_payload(payload),
        attributes=dict(msg.message.attributes),
    )
    client.acknowledge(
        subscription=subscription_path(subscription), ack_ids=[msg.ack_id]
    )
    return item.__dict__
