"""Consume one message from a Google Cloud Pub/Sub managed subscription.

Uses the google-cloud-pubsub SDK to pull a single message from a
configured subscription. Authentication relies on
GOOGLE_APPLICATION_CREDENTIALS.
"""

from typing import Optional

from google.cloud.pubsub_v1.types import (
    Subscription,
    ReceivedMessage as PubsubReceivedMessage,
)
from google.cloud import pubsub_v1

from messaging_client import (
    get_subscriber,
    subscription_path,
    decode_message_data,
)
from messaging_models import ConsumedMessage


def consume_event(
    subscription_id: Optional[str] = None,
    timeout: float = 10.0,
) -> Optional[ConsumedMessage]:
    """Pull exactly one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: Override the default subscription name.
        timeout: Maximum seconds to wait for a message.

    Returns:
        ConsumedMessage if one is available, otherwise None.
    """
    subscriber: pubsub_v1.SubscriberClient = get_subscriber()
    sub_path = subscription_path(subscription_id)

    response = subscriber.pull(
        subscription=sub_path,
        max_messages=1,
        timeout=timeout,
    )

    received_messages = response.received_messages
    if not received_messages:
        return None

    pubsub_msg: PubsubReceivedMessage = received_messages[0]
    msg = pubsub_msg.message

    data = decode_message_data(msg.data)
    attrs = dict(msg.attributes)

    consumed = ConsumedMessage(
        message_id=msg.message_id,
        event_id=attrs.get("event_id", ""),
        event_type=attrs.get("event_type", "unknown"),
        source=attrs.get("source", "unknown"),
        payload=data,
        attributes=attrs,
    )

    # Acknowledge the message so it is not redelivered
    subscriber.acknowledge(
        subscription=sub_path,
        ack_ids=[pubsub_msg.ack_id],
    )
    consumed.acknowledged = True

    return consumed


if __name__ == "__main__":
    result = consume_event(timeout=5.0)
    if result:
        print(f"Received event_id={result.event_id}, type={result.event_type}")
    else:
        print("No messages available.")
