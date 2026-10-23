from __future__ import annotations

from messaging_client import get_pubsub_subscriber, pubsub_subscription_path
from messaging_models import ConsumedMessage, decode_payload


def consume_event(ack: bool = False) -> ConsumedMessage | None:
    subscriber = get_pubsub_subscriber()
    response = subscriber.pull(
        request={
            "subscription": pubsub_subscription_path(),
            "max_messages": 1,
        },
        timeout=10,
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    message = received.message
    if ack:
        subscriber.acknowledge(
            request={
                "subscription": pubsub_subscription_path(),
                "ack_ids": [received.ack_id],
            }
        )
    return ConsumedMessage(
        ack_id=received.ack_id,
        message_id=message.message_id,
        payload=decode_payload(message.data),
        attributes=dict(message.attributes),
        publish_time=message.publish_time.isoformat() if message.publish_time else None,
        delivery_attempt=received.delivery_attempt,
    )
