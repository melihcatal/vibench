from __future__ import annotations

import json
from typing import Optional

from messaging_client import PUBSUB_PROVIDER, get_subscription_path, subscriber_client
from messaging_models import ConsumedMessage


def consume_event(
    subscription_path: Optional[str] = None, ack: bool = False
) -> Optional[ConsumedMessage]:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": get_subscription_path(subscription_path),
            "max_messages": 1,
        }
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    message = received.message
    if ack:
        client.acknowledge(
            request={
                "subscription": get_subscription_path(subscription_path),
                "ack_ids": [received.ack_id],
            }
        )
    payload = json.loads(message.data.decode("utf-8")) if message.data else {}
    publish_time = message.publish_time.isoformat() if message.publish_time else None
    return ConsumedMessage(
        provider=PUBSUB_PROVIDER,
        subscription=get_subscription_path(subscription_path),
        ack_id=received.ack_id,
        message_id=message.message_id,
        payload=payload,
        attributes=dict(message.attributes),
        publish_time=publish_time,
    )
