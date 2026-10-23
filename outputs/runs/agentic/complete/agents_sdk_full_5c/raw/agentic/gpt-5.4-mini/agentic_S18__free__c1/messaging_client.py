from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str
    dead_letter_subscription_id: str


@lru_cache(maxsize=1)
def load_config() -> MessagingConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "demo-project")
    topic_id = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
    dead_letter_topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dlq")
    dead_letter_subscription_id = os.environ.get("PUBSUB_DEAD_LETTER_SUBSCRIPTION_ID", "events-dlq-subscription")
    return MessagingConfig(
        project_id=project_id,
        topic_id=topic_id,
        subscription_id=subscription_id,
        dead_letter_topic_id=dead_letter_topic_id,
        dead_letter_subscription_id=dead_letter_subscription_id,
    )


@lru_cache(maxsize=1)
def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: Optional[str] = None) -> str:
    cfg = load_config()
    return publisher_client().topic_path(cfg.project_id, topic_id or cfg.topic_id)


def subscription_path(subscription_id: Optional[str] = None) -> str:
    cfg = load_config()
    return subscriber_client().subscription_path(cfg.project_id, subscription_id or cfg.subscription_id)


def dead_letter_topic_path(topic_id: Optional[str] = None) -> str:
    cfg = load_config()
    return publisher_client().topic_path(cfg.project_id, topic_id or cfg.dead_letter_topic_id)


def dead_letter_subscription_path(subscription_id: Optional[str] = None) -> str:
    cfg = load_config()
    return subscriber_client().subscription_path(cfg.project_id, subscription_id or cfg.dead_letter_subscription_id)
