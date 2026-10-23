from __future__ import annotations

import os
from typing import Optional

from google.cloud import pubsub_v1


PUBSUB_PROJECT_ID_ENV = "GCP_PROJECT_ID"
PUBSUB_TOPIC_ENV = "PUBSUB_TOPIC_ID"
PUBSUB_SUBSCRIPTION_ENV = "PUBSUB_SUBSCRIPTION_ID"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "PUBSUB_DEAD_LETTER_TOPIC_ID"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def get_project_id() -> str:
    project_id = os.getenv(PUBSUB_PROJECT_ID_ENV)
    if not project_id:
        raise ValueError(f"Missing environment variable: {PUBSUB_PROJECT_ID_ENV}")
    return project_id


def get_topic_id(default: Optional[str] = None) -> str:
    topic_id = os.getenv(PUBSUB_TOPIC_ENV, default or "")
    if not topic_id:
        raise ValueError(f"Missing environment variable: {PUBSUB_TOPIC_ENV}")
    return topic_id


def get_subscription_id(default: Optional[str] = None) -> str:
    subscription_id = os.getenv(PUBSUB_SUBSCRIPTION_ENV, default or "")
    if not subscription_id:
        raise ValueError(f"Missing environment variable: {PUBSUB_SUBSCRIPTION_ENV}")
    return subscription_id


def get_dead_letter_topic_id(default: Optional[str] = None) -> str:
    topic_id = os.getenv(PUBSUB_DEAD_LETTER_TOPIC_ENV, default or "")
    if not topic_id:
        raise ValueError(f"Missing environment variable: {PUBSUB_DEAD_LETTER_TOPIC_ENV}")
    return topic_id


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: Optional[str] = None) -> str:
    client = publisher_client()
    return client.topic_path(get_project_id(), topic_id or get_topic_id())


def subscription_path(subscription_id: Optional[str] = None) -> str:
    client = subscriber_client()
    return client.subscription_path(get_project_id(), subscription_id or get_subscription_id())


def dead_letter_topic_path(topic_id: Optional[str] = None) -> str:
    client = publisher_client()
    return client.topic_path(get_project_id(), topic_id or get_dead_letter_topic_id())
