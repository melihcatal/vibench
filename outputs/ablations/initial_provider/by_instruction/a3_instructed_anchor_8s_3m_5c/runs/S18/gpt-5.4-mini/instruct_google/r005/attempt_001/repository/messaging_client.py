import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


@dataclass
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic: str


def load_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        topic_id=os.environ.get("PUBSUB_TOPIC_ID", "events-topic"),
        subscription_id=os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription"),
        dead_letter_topic=os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "events-dead-letter"),
    )


def topic_path(project_id: str, topic_id: str) -> str:
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def ensure_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode("utf-8")
    return str(value).encode("utf-8")


def build_attributes(attributes: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (attributes or {}).items()}
