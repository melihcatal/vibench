from __future__ import annotations

from messaging_client import subscriber_client, subscription_path
from messaging_models import ConsumedMessage, decode_message_bytes


PROVIDER = "google-cloud-pubsub"


def consume_one_message() -> ConsumedMessage | None:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": subscription_path(),
            "max_messages": 1,
        },
        timeout=15,
    )
    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message
    payload = decode_message_bytes(message.data)
    client.acknowledge(
        request={
            "subscription": subscription_path(),
            "ack_ids": [received.ack_id],
        }
    )
    return ConsumedMessage(
        ack_id=received.ack_id,
        message_id=message.message_id,
        data=payload,
        attributes=dict(message.attributes),
        publish_time=message.publish_time.isoformat() if message.publish_time else None,
        ordering_key=message.ordering_key or None,
    )
