from __future__ import annotations

import os
from typing import Optional

from google.cloud import pubsub_v1


PUBSUB_PROJECT_ID_ENV = "GCP_PROJECT_ID"
PUBSUB_TOPIC_ENV = "PUBSUB_TOPIC_ID"
PUBSUB_SUBSCRIPTION_ENV = "PUBSUB_SUBSCRIPTION_ID"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "PUBSUB_DEAD_LETTER_TOPIC_ID"


def get_project_id(explicit: Optional[str] = None) -> str:
    project_id = explicit or os.getenv(PUBSUB_PROJECT_ID_ENV) or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Missing Google Cloud project id. Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT.")
    return project_id


def get_topic_id(explicit: Optional[str] = None) -> str:
    topic_id = explicit or os.getenv(PUBSUB_TOPIC_ENV)
    if not topic_id:
        raise ValueError("Missing Pub/Sub topic id. Set PUBSUB_TOPIC_ID.")
    return topic_id


def get_subscription_id(explicit: Optional[str] = None) -> str:
    subscription_id = explicit or os.getenv(PUBSUB_SUBSCRIPTION_ENV)
    if not subscription_id:
        raise ValueError("Missing Pub/Sub subscription id. Set PUBSUB_SUBSCRIPTION_ID.")
    return subscription_id


def get_dead_letter_topic_id(explicit: Optional[str] = None) -> str:
    topic_id = explicit or os.getenv(PUBSUB_DEAD_LETTER_TOPIC_ENV)
    if not topic_id:
        raise ValueError("Missing dead-letter topic id. Set PUBSUB_DEAD_LETTER_TOPIC_ID.")
    return topic_id


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = publisher_client()
    return client.topic_path(get_project_id(project_id), get_topic_id(topic_id))


def dead_letter_topic_path(topic_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = publisher_client()
    return client.topic_path(get_project_id(project_id), get_dead_letter_topic_id(topic_id))


def subscription_path(subscription_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = subscriber_client()
    return client.subscription_path(get_project_id(project_id), get_subscription_id(subscription_id))
