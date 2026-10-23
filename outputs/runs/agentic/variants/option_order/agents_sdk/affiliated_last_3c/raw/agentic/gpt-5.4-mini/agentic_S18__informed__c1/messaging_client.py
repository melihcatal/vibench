from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os
from typing import Any

from google.cloud import pubsub_v1


@dataclass(frozen=True, slots=True)
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str


@lru_cache(maxsize=1)
def get_config() -> MessagingConfig:
    return MessagingConfig(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT", "demo-project")),
        topic_id=os.environ.get("PUBSUB_TOPIC_ID", "events-topic"),
        subscription_id=os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription"),
        dead_letter_topic_id=os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter"),
    )


@lru_cache(maxsize=1)
def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: str | None = None) -> str:
    cfg = get_config()
    return get_publisher().topic_path(cfg.project_id, topic_id or cfg.topic_id)


def subscription_path(subscription_id: str | None = None) -> str:
    cfg = get_config()
    return get_subscriber().subscription_path(cfg.project_id, subscription_id or cfg.subscription_id)


def dead_letter_topic_path(topic_id: str | None = None) -> str:
    cfg = get_config()
    return get_publisher().topic_path(cfg.project_id, topic_id or cfg.dead_letter_topic_id)


def to_pubsub_attributes(attributes: dict[str, Any] | None) -> dict[str, str]:
    if not attributes:
        return {}
    return {str(k): "" if v is None else str(v) for k, v in attributes.items()}
