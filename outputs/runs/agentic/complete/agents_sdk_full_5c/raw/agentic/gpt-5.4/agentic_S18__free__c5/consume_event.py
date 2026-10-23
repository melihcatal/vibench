from __future__ import annotations

import json
from typing import Optional

from google.cloud.pubsub_v1.subscriber.message import Message

from messaging_client import subscriber_client, subscription_path
from messaging_models import ConsumedMessage


def consume_event(ack: bool = True, timeout: Optional[int] = 10) -> Optional[ConsumedMessage]:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": subscription_path(),
            "max_messages": 1,
        },
        timeout=timeout,
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    msg = received.message
    if ack:
        client.acknowledge(
            request={
                "subscription": subscription_path(),
                "ack_ids": [received.ack_id],
            }
        )
    data = json.loads(msg.data.decode("utf-8"))
    return ConsumedMessage(
        ack_id=received.ack_id,
        message_id=msg.message_id,
        data=data,
        attributes=dict(msg.attributes),
        publish_time=msg.publish_time.isoformat() if msg.publish_time else None,
    )
