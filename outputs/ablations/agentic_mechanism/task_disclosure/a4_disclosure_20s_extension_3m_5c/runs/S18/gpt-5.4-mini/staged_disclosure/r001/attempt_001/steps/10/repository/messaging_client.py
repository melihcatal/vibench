import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None
    credentials_path: Optional[str] = None


def load_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=os.environ["GOOGLE_CLOUD_PROJECT"],
        topic_id=os.getenv("PUBSUB_TOPIC_ID"),
        subscription_id=os.getenv("PUBSUB_SUBSCRIPTION_ID"),
        credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    )


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_id: str) -> str:
    return get_publisher_client().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return get_subscriber_client().subscription_path(project_id, subscription_id)


def publish_message(topic_id: str, data: bytes, project_id: Optional[str] = None, **attributes: str) -> str:
    cfg = load_config()
    resolved_project_id = project_id or cfg.project_id
    future = get_publisher_client().publish(topic_path(resolved_project_id, topic_id), data, **attributes)
    return future.result()


def pull_messages(subscription_id: str, project_id: Optional[str] = None, max_messages: int = 10, timeout: float = 10.0):
    cfg = load_config()
    resolved_project_id = project_id or cfg.project_id
    response = get_subscriber_client().pull(
        subscription=subscription_path(resolved_project_id, subscription_id),
        max_messages=max_messages,
        timeout=timeout,
    )
    return response.received_messages
