import json

from google.cloud import pubsub_v1

from messaging_client import get_subscriber_client, subscription_path
from messaging_models import ConsumeResponse, normalize_message_payload


def consume_event(subscription: str, timeout: float = 10.0) -> ConsumeResponse:
    client = get_subscriber_client()
    response = client.pull(
        request={"subscription": subscription_path(subscription), "max_messages": 1},
        timeout=timeout,
    )
    if not response.received_messages:
        return ConsumeResponse(message_id=None, payload={})
    msg = response.received_messages[0]
    payload = normalize_message_payload(msg.message.data)
    client.acknowledge(
        request={
            "subscription": subscription_path(subscription),
            "ack_ids": [msg.ack_id],
        }
    )
    return ConsumeResponse(
        message_id=msg.message.message_id,
        payload=payload,
        attributes=dict(msg.message.attributes),
    )
