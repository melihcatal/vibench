import os
from typing import Optional

from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.cloud.pubsub_v1.types import (
    PublisherOptions,
    Subscription,
    DeadLetterPolicy,
    RetryPolicy,
)

PROJECT_ID_ENV = "GCP_PROJECT_ID"
PUBSUB_TOPIC_ENV = "PUBSUB_TOPIC_ID"
PUBSUB_SUBSCRIPTION_ENV = "PUBSUB_SUBSCRIPTION_ID"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "PUBSUB_DEAD_LETTER_TOPIC_ID"


def get_project_id() -> str:
    project_id = os.environ.get(PROJECT_ID_ENV)
    if not project_id:
        raise ValueError(f"Environment variable {PROJECT_ID_ENV} is required")
    return project_id


def get_topic_path() -> str:
    project_id = get_project_id()
    topic_id = os.environ.get(PUBSUB_TOPIC_ENV, "events-topic")
    return f"projects/{project_id}/topics/{topic_id}"


def get_subscription_path() -> str:
    project_id = get_project_id()
    subscription_id = os.environ.get(PUBSUB_SUBSCRIPTION_ENV, "events-subscription")
    return f"projects/{project_id}/subscriptions/{subscription_id}"


def get_dead_letter_topic_path() -> str:
    project_id = get_project_id()
    dead_letter_topic_id = os.environ.get(
        PUBSUB_DEAD_LETTER_TOPIC_ENV, "events-dead-letter"
    )
    return f"projects/{project_id}/topics/{dead_letter_topic_id}"


def get_dead_letter_subscription_path() -> str:
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/events-dead-letter-sub"


def create_publisher_client() -> PublisherClient:
    publisher_options = PublisherOptions(
        flow_control=PublisherOptions.FlowControl(max_messages=1000),
        enable_message_ordering=False,
    )
    return PublisherClient(publisher_options=publisher_options)


def create_subscriber_client() -> SubscriberClient:
    return SubscriberClient()


def ensure_topic_exists(publisher: PublisherClient, topic_path: str) -> None:
    try:
        publisher.get_topic(request={"name": topic_path})
    except Exception:
        publisher.create_topic(request={"name": topic_path})


def ensure_subscription_exists(
    subscriber: SubscriberClient,
    subscription_path: str,
    topic_path: str,
    dead_letter_topic_path: Optional[str] = None,
    max_delivery_attempts: int = 5,
) -> Subscription:
    try:
        return subscriber.get_subscription(request={"subscription": subscription_path})
    except Exception:
        sub_config = {"name": subscription_path, "topic": topic_path}

        if dead_letter_topic_path:
            dead_letter_policy = DeadLetterPolicy(
                dead_letter_topic=dead_letter_topic_path,
                max_delivery_attempts=max_delivery_attempts,
            )
            sub_config["dead_letter_policy"] = dead_letter_policy

        retry_policy = RetryPolicy(
            minimum_backoff=10.0,
            maximum_backoff=600.0,
        )
        sub_config["retry_policy"] = retry_policy

        return subscriber.create_subscription(request=sub_config)


def build_message_data(payload_bytes: bytes, attributes: Optional[dict] = None) -> dict:
    message = {"data": payload_bytes}
    if attributes:
        message["attributes"] = attributes
    return message


def extract_message_text(message) -> str:
    try:
        return message.data.decode("utf-8")
    except Exception:
        return ""


def extract_message_attributes(message) -> dict:
    return dict(message.attributes) if message.attributes else {}


def acknowledge_message(
    subscriber: SubscriberClient, subscription_path: str, ack_id: str
) -> None:
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]}
    )


def nack_message(
    subscriber: SubscriberClient, subscription_path: str, ack_id: str
) -> None:
    subscriber.modify_ack_deadline(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
            "ack_deadline_seconds": 0,
        }
    )
