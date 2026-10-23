import os
from typing import Optional
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
PUBSUB_TOPIC_NAME = os.environ.get("PUBSUB_TOPIC_NAME", "events-topic")
PUBSUB_SUBSCRIPTION_NAME = os.environ.get(
    "PUBSUB_SUBSCRIPTION_NAME", "events-subscription"
)
PUBSUB_DEAD_LETTER_TOPIC_NAME = os.environ.get(
    "PUBSUB_DEAD_LETTER_TOPIC_NAME", "events-dead-letter"
)

_publisher: Optional[pubsub_v1.PublisherClient] = None
_subscriber: Optional[pubsub_v1.SubscriberClient] = None


def get_publisher() -> pubsub_v1.PublisherClient:
    global _publisher
    if _publisher is None:
        _publisher = pubsub_v1.PublisherClient()
    return _publisher


def get_subscriber() -> pubsub_v1.SubscriberClient:
    global _subscriber
    if _subscriber is None:
        _subscriber = pubsub_v1.SubscriberClient()
    return _subscriber


def topic_path(
    project_id: Optional[str] = None, topic_name: Optional[str] = None
) -> str:
    pid = project_id or PROJECT_ID
    name = topic_name or PUBSUB_TOPIC_NAME
    return f"projects/{pid}/topics/{name}"


def subscription_path(
    project_id: Optional[str] = None, subscription_name: Optional[str] = None
) -> str:
    pid = project_id or PROJECT_ID
    name = subscription_name or PUBSUB_SUBSCRIPTION_NAME
    return f"projects/{pid}/subscriptions/{name}"


def dead_letter_topic_path(
    project_id: Optional[str] = None, topic_name: Optional[str] = None
) -> str:
    pid = project_id or PROJECT_ID
    name = topic_name or PUBSUB_DEAD_LETTER_TOPIC_NAME
    return f"projects/{pid}/topics/{name}"


def publish_message(
    topic: str,
    data: bytes,
    attributes: Optional[dict] = None,
) -> str:
    publisher = get_publisher()
    future = publisher.publish(topic, data, **(attributes or {}))
    return future.result()


def pull_message(
    subscription: str,
    max_messages: int = 1,
) -> list:
    subscriber = get_subscriber()
    response = subscriber.pull(
        request={"subscription": subscription, "max_messages": max_messages}
    )
    return list(response.received_messages)


def acknowledge_message(subscription: str, ack_id: str) -> None:
    subscriber = get_subscriber()
    subscriber.acknowledge(request={"subscription": subscription, "ack_ids": [ack_id]})


def modify_ack_deadline(
    subscription: str, ack_id: str, deadline_seconds: int = 0
) -> None:
    subscriber = get_subscriber()
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": deadline_seconds,
        }
    )


def validate_config() -> list[str]:
    errors = []
    if not PROJECT_ID:
        errors.append("GOOGLE_CLOUD_PROJECT environment variable is not set")
    return errors
