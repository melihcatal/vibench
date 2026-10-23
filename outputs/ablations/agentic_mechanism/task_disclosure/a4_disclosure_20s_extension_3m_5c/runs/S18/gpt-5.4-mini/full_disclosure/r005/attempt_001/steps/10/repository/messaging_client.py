import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_path: Optional[str] = None
    subscription_path: Optional[str] = None
    credentials_path: Optional[str] = None


def load_messaging_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        topic_path=os.environ.get("PUBSUB_TOPIC_PATH"),
        subscription_path=os.environ.get("PUBSUB_SUBSCRIPTION_PATH"),
        credentials_path=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
    )


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def build_topic_path(project_id: str, topic_id: str) -> str:
    return get_publisher_client().topic_path(project_id, topic_id)


def build_subscription_path(project_id: str, subscription_id: str) -> str:
    return get_subscriber_client().subscription_path(project_id, subscription_id)


def resolve_topic_path(topic_path: Optional[str] = None) -> str:
    if topic_path:
        return topic_path
    config = load_messaging_config()
    if config.topic_path:
        return config.topic_path
    if not config.project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required to resolve a topic path")
    raise ValueError("PUBSUB_TOPIC_PATH is required or provide topic_path")


def resolve_subscription_path(subscription_path: Optional[str] = None) -> str:
    if subscription_path:
        return subscription_path
    config = load_messaging_config()
    if config.subscription_path:
        return config.subscription_path
    if not config.project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required to resolve a subscription path")
    raise ValueError("PUBSUB_SUBSCRIPTION_PATH is required or provide subscription_path")
