"""
Local configuration and client helper utilities for Pub/Sub Messaging.
Provides Google Cloud Pub/Sub client setup and utility functions.
"""

import os
from typing import Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError


def get_pubsub_publisher_client() -> pubsub_v1.PublisherClient:
    """
    Create and return a Google Cloud Pub/Sub publisher client.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable for auth.
    """
    return pubsub_v1.PublisherClient()


def get_pubsub_subscriber_client() -> pubsub_v1.SubscriberClient:
    """
    Create and return a Google Cloud Pub/Sub subscriber client.
    Uses GOOGLE_APPLICATION_CREDENTIALS environment variable for auth.
    """
    return pubsub_v1.SubscriberClient()


def get_topic_path(project_id: Optional[str] = None, topic_id: str = "events-topic") -> str:
    """Build a fully-qualified Pub/Sub topic path."""
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
    return pubsub_v1.PublisherClient.topic_path(project, topic_id)


def get_subscription_path(
    project_id: Optional[str] = None, subscription_id: str = "events-subscription"
) -> str:
    """Build a fully-qualified Pub/Sub subscription path."""
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
    return pubsub_v1.SubscriberClient.subscription_path(project, subscription_id)


def get_dead_letter_topic_path(
    project_id: Optional[str] = None, topic_id: str = "dead-letter-events"
) -> str:
    """Build a fully-qualified dead-letter topic path."""
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
    return pubsub_v1.PublisherClient.topic_path(project, topic_id)


def get_dead_letter_subscription_path(
    project_id: Optional[str] = None, subscription_id: str = "dead-letter-subscription"
) -> str:
    """Build a fully-qualified dead-letter subscription path."""
    project = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
    return pubsub_v1.SubscriberClient.subscription_path(project, subscription_id)


def publish_with_retry(
    publisher: pubsub_v1.PublisherClient,
    topic_path: str,
    message_bytes: bytes,
    attributes: Optional[dict] = None,
    max_retries: int = 3,
) -> str:
    """
    Publish a message to a Pub/Sub topic with retry logic.
    Returns the message ID on success.
    """
    future = publisher.publish(topic_path, data=message_bytes, **(attributes or {}))
    try:
        message_id = future.result(timeout=30)
        return message_id
    except GoogleAPIError:
        if max_retries > 0:
            return publish_with_retry(publisher, topic_path, message_bytes, attributes, max_retries - 1)
        raise


def consume_one_message(
    subscriber: pubsub_v1.SubscriberClient,
    subscription_path: str,
    timeout_seconds: float = 10.0,
) -> Optional[dict]:
    """
    Pull and return exactly one message from a Pub/Sub subscription.
    Returns a dict with 'message_id', 'data', and 'attributes', or None.
    """
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1},
        timeout=timeout_seconds,
    )
    if not response.received_messages:
        return None
    msg = response.received_messages[0].message
    return {
        "message_id": msg.message_id,
        "data": msg.data.decode("utf-8"),
        "attributes": dict(msg.attributes),
        "ack_id": response.received_messages[0].ack_id,
    }


def ack_message(subscriber: pubsub_v1.SubscriberClient, subscription_path: str, ack_id: str) -> None:
    """Acknowledge a message by its ack ID."""
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]},
    )


def nak_message(subscriber: pubsub_v1.SubscriberClient, subscription_path: str, ack_id: str) -> None:
    """Negative-acknowledge (nack) a message for redelivery."""
    subscriber.modify_ack_deadline(
        request={"subscription": subscription_path, "ack_ids": [ack_id], "ack_deadline_seconds": 0},
    )
