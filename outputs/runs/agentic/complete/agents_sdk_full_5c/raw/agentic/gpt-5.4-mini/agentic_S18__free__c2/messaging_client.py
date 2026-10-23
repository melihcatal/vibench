from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1

DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
DEFAULT_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events")
DEFAULT_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
DEFAULT_DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dlq")


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: str = DEFAULT_TOPIC_ID
    subscription_id: str = DEFAULT_SUBSCRIPTION_ID
    dead_letter_topic_id: str = DEFAULT_DEAD_LETTER_TOPIC_ID


def load_config(project_id: Optional[str] = None) -> MessagingConfig:
    resolved_project = project_id or DEFAULT_PROJECT_ID
    if not resolved_project:
        raise ValueError("Google Cloud project id is required via GOOGLE_CLOUD_PROJECT or argument")
    return MessagingConfig(project_id=resolved_project)


@lru_cache(maxsize=1)
def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(config: MessagingConfig) -> str:
    return publisher_client().topic_path(config.project_id, config.topic_id)


def subscription_path(config: MessagingConfig) -> str:
    return subscriber_client().subscription_path(config.project_id, config.subscription_id)


def dead_letter_topic_path(config: MessagingConfig) -> str:
    return publisher_client().topic_path(config.project_id, config.dead_letter_topic_id)
