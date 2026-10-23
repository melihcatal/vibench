import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import pubsub_v1


@dataclass
class MessagingConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None
    dead_letter_topic_id: Optional[str] = None


def load_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        topic_id=os.getenv("PUBSUB_TOPIC_ID"),
        subscription_id=os.getenv("PUBSUB_SUBSCRIPTION_ID"),
        dead_letter_topic_id=os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID"),
    )


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(config: MessagingConfig, topic_id: Optional[str] = None) -> str:
    return publisher_client().topic_path(config.project_id, topic_id or config.topic_id or "")


def subscription_path(config: MessagingConfig, subscription_id: Optional[str] = None) -> str:
    return subscriber_client().subscription_path(config.project_id, subscription_id or config.subscription_id or "")
