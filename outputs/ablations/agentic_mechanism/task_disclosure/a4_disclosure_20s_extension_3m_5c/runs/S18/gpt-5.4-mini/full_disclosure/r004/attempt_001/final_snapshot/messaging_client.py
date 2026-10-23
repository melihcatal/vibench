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
    location: Optional[str] = None


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value is not None and value != "" else default


def load_config() -> MessagingConfig:
    project_id = _env("GOOGLE_CLOUD_PROJECT") or _env("GCLOUD_PROJECT") or _env("PUBSUB_PROJECT_ID")
    if not project_id:
        raise ValueError("Missing Google Cloud project configuration")
    return MessagingConfig(
        project_id=project_id,
        topic_id=_env("PUBSUB_TOPIC_ID"),
        subscription_id=_env("PUBSUB_SUBSCRIPTION_ID"),
        location=_env("PUBSUB_LOCATION"),
    )


def topic_path(project_id: str, topic_id: str) -> str:
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)


@lru_cache(maxsize=1)
def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def resolve_topic_path(topic_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    cfg = load_config()
    return topic_path(project_id or cfg.project_id, topic_id or cfg.topic_id or "")


def resolve_subscription_path(subscription_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    cfg = load_config()
    return subscription_path(project_id or cfg.project_id, subscription_id or cfg.subscription_id or "")
