"""Consume one message from a Google Cloud Pub/Sub managed subscription."""

import json
from typing import Optional

from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from messaging_client import get_pubsub_subscriber_client, get_pubsub_config
from messaging_models import ConsumedMessage, MessageAck


def consume_event(subscription_id: str, timeout: float = 30.0) -> Optional[ConsumedMessage]:
    """Consume a single message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: Google Cloud Pub/Sub subscription name.
        timeout: Maximum seconds to wait for a message.

    Returns:
        ConsumedMessage with payload and metadata, or None if timeout.
    """
    config = get_pubsub_config()
    project_id = config["project_id"]

    subscriber_client = get_pubsub_subscriber_client()
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    response = subscriber_client.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    pubsub_message: Message = received.message

    try:
        payload = json.loads(pubsub_message.data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = pubsub_message.data.decode("utf-8", errors="replace")

    attributes = dict(pubsub_message.attributes)
    message_id = pubsub_message.message_id

    ack_id = received.ack_id

    return ConsumedMessage(
        message_id=message_id,
        ack_id=ack_id,
        subscription_path=subscription_path,
        payload=payload,
        attributes=attributes,
        publish_time=received.message.publish_time.isoformat() if received.message.publish_time else None,
    )


def consume_and_ack(subscription_id: str, timeout: float = 30.0) -> Optional[ConsumedMessage]:
    """Consume a message and automatically acknowledge it via Google Cloud Pub/Sub.

    Args:
        subscription_id: Google Cloud Pub/Sub subscription name.
        timeout: Maximum seconds to wait for a message.

    Returns:
        ConsumedMessage with payload, or None if no message.
    """
    config = get_pubsub_config()
    project_id = config["project_id"]

    subscriber_client = get_pubsub_subscriber_client()
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    response = subscriber_client.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=timeout,
    )

    if not response.received_messages:
        return None

    received = response.received_messages[0]
    pubsub_message: Message = received.message

    try:
        payload = json.loads(pubsub_message.data.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = pubsub_message.data.decode("utf-8", errors="replace")

    ack_id = received.ack_id
    subscriber_client.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]}
    )

    return ConsumedMessage(
        message_id=pubsub_message.message_id,
        ack_id=ack_id,
        subscription_path=subscription_path,
        payload=payload,
        attributes=dict(pubsub_message.attributes),
        publish_time=received.message.publish_time.isoformat() if received.message.publish_time else None,
    )
