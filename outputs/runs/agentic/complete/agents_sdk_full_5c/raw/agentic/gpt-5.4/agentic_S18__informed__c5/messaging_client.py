from __future__ import annotations

import os
from typing import Optional

from google.cloud import pubsub_v1


PUBSUB_PROVIDER = "google-cloud-pubsub"
PUBSUB_TOPIC_ENV = "GCP_PUBSUB_TOPIC"
PUBSUB_SUBSCRIPTION_ENV = "GCP_PUBSUB_SUBSCRIPTION"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "GCP_PUBSUB_DEAD_LETTER_TOPIC"
GOOGLE_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def get_topic_path(explicit_topic: Optional[str] = None) -> str:
    topic = explicit_topic or os.getenv(PUBSUB_TOPIC_ENV)
    if not topic:
        raise ValueError(f"Missing Pub/Sub topic. Set {PUBSUB_TOPIC_ENV} to a full topic path.")
    return topic


def get_subscription_path(explicit_subscription: Optional[str] = None) -> str:
    subscription = explicit_subscription or os.getenv(PUBSUB_SUBSCRIPTION_ENV)
    if not subscription:
        raise ValueError(f"Missing Pub/Sub subscription. Set {PUBSUB_SUBSCRIPTION_ENV} to a full subscription path.")
    return subscription


def get_dead_letter_topic_path(explicit_topic: Optional[str] = None) -> str:
    topic = explicit_topic or os.getenv(PUBSUB_DEAD_LETTER_TOPIC_ENV)
    if not topic:
        raise ValueError(
            f"Missing dead-letter topic. Set {PUBSUB_DEAD_LETTER_TOPIC_ENV} to a full topic path."
        )
    return topic
