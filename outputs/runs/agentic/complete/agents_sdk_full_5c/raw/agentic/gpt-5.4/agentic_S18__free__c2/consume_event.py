from __future__ import annotations

import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import subscriber_client, subscription_path
from messaging_models import ConsumedMessage


Message = pubsub_v1.subscriber.message.Message


def consume_one_message(
    *,
    subscription_id: Optional[str] = None,
    project_id: Optional[str] = None,
    acknowledge: bool = False,
) -> Optional[ConsumedMessage]:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": subscription_path(subscription_id=subscription_id, project_id=project_id),
            "max_messages": 1,
        },
        timeout=10,
    )
    if not response.received_messages:
        return None

    received = response.received_messages[0]
    msg: Message = received.message
    if acknowledge:
        client.acknowledge(
            request={
                "subscription": subscription_path(subscription_id=subscription_id, project_id=project_id),
                "ack_ids": [received.ack_id],
            }
        )

    return ConsumedMessage(
        ack_id=received.ack_id,
        message_id=msg.message_id,
        payload=json.loads(msg.data.decode("utf-8")),
        attributes=dict(msg.attributes),
        publish_time=msg.publish_time.isoformat() if msg.publish_time else None,
        ordering_key=msg.ordering_key or None,
    )
