from __future__ import annotations

import json
from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import get_config, get_subscriber_client
from messaging_models import ConsumedMessage


GOOGLE_PUBSUB_PROVIDER = "google-cloud-pubsub"


def consume_one_message(ack: bool = False) -> Optional[ConsumedMessage]:
    config = get_config()
    subscriber: pubsub_v1.SubscriberClient = get_subscriber_client()

    response = subscriber.pull(
        request={
            "subscription": config.subscription_path,
            "max_messages": 1,
        },
        retry=None,
        timeout=10,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    message = received.message
    payload = json.loads(message.data.decode("utf-8"))

    if ack:
        subscriber.acknowledge(
            request={
                "subscription": config.subscription_path,
                "ack_ids": [received.ack_id],
            }
        )

    return ConsumedMessage(
        ack_id=received.ack_id,
        payload=payload,
        attributes=dict(message.attributes),
        message_id=message.message_id,
        publish_time=str(message.publish_time),
    )
