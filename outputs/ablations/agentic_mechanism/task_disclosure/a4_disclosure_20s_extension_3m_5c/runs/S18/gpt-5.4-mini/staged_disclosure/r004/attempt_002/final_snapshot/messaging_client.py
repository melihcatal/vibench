import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class PubSubConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None
    credentials_path: Optional[str] = None


def load_config() -> PubSubConfig:
    return PubSubConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        topic_id=os.environ.get("PUBSUB_TOPIC_ID"),
        subscription_id=os.environ.get("PUBSUB_SUBSCRIPTION_ID"),
        credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
    )


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_id: str) -> str:
    return get_publisher_client().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return get_subscriber_client().subscription_path(project_id, subscription_id)


def publish_message(project_id: str, topic_id: str, data: bytes, **attributes: str) -> str:
    client = get_publisher_client()
    topic = client.topic_path(project_id, topic_id)
    future = client.publish(topic, data, **attributes)
    return future.result()


def pull_messages(
    project_id: str,
    subscription_id: str,
    max_messages: int = 1,
    timeout: float = 5.0,
):
    client = get_subscriber_client()
    subscription = client.subscription_path(project_id, subscription_id)
    response = client.pull(subscription=subscription, max_messages=max_messages, timeout=timeout)
    return response.received_messages
