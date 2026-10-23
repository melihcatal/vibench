from __future__ import annotations

import os
from typing import Optional

from google.cloud import pubsub_v1


PUBSUB_PROVIDER = "google-cloud-pubsub"
PUBSUB_TOPIC_ENV = "GCP_PUBSUB_TOPIC"
PUBSUB_SUBSCRIPTION_ENV = "GCP_PUBSUB_SUBSCRIPTION"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "GCP_PUBSUB_DEAD_LETTER_TOPIC"


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def get_topic_path(topic_path: Optional[str] = None) -> str:
    return topic_path or require_env(PUBSUB_TOPIC_ENV)


def get_subscription_path(subscription_path: Optional[str] = None) -> str:
    return subscription_path or require_env(PUBSUB_SUBSCRIPTION_ENV)


def get_dead_letter_topic_path(topic_path: Optional[str] = None) -> str:
    return topic_path or require_env(PUBSUB_DEAD_LETTER_TOPIC_ENV)


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()
