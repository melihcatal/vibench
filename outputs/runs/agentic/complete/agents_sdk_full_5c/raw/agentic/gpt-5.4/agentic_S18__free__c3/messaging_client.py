from __future__ import annotations

import os
from typing import Optional

from google.cloud import pubsub_v1


GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
PUBSUB_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
PUBSUB_DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter")


class PubSubConfigError(ValueError):
    pass


def require_project_id(project_id: Optional[str] = None) -> str:
    resolved = project_id or GOOGLE_CLOUD_PROJECT
    if not resolved:
        raise PubSubConfigError("GOOGLE_CLOUD_PROJECT is required for Google Cloud Pub/Sub")
    return resolved


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = publisher_client()
    return client.topic_path(require_project_id(project_id), topic_id or PUBSUB_TOPIC_ID)


def dead_letter_topic_path(topic_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = publisher_client()
    return client.topic_path(require_project_id(project_id), topic_id or PUBSUB_DEAD_LETTER_TOPIC_ID)


def subscription_path(subscription_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = subscriber_client()
    return client.subscription_path(require_project_id(project_id), subscription_id or PUBSUB_SUBSCRIPTION_ID)
