from __future__ import annotations

from typing import Optional

from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import ConsumedMessage, decode_message_data


def consume_one(subscription: Optional[str] = None, auto_ack: bool = True, timeout: float = 10.0) -> Optional[ConsumedMessage]:
    subscriber = get_subscriber_client()
    subscription_path = get_subscription_path(subscription)
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        },
        timeout=timeout,
    )
    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message
    if auto_ack:
        subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [received.ack_id],
            }
        )

    return ConsumedMessage(
        ack_id=received.ack_id,
        message_id=message.message_id,
        data=decode_message_data(message.data),
        attributes=dict(message.attributes),
        publish_time=message.publish_time.isoformat() if message.publish_time else None,
    )
