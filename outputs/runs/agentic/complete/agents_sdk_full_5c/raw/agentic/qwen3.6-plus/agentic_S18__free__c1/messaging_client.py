"""messaging_client.py - Configuration and client helper utilities for Google Cloud Pub/Sub Messaging."""

import os
from functools import lru_cache
from google.cloud import pubsub_v1


# Google Cloud Pub/Sub configuration
PUBSUB_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-gcp-project-id")
PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
PUBSUB_SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
PUBSUB_DEAD_LETTER_TOPIC_ID = os.environ.get(
    "PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter-topic"
)

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/service-account.json"
)


@lru_cache(maxsize=2)
def get_pubsub_publisher_client() -> pubsub_v1.PublisherClient:
    """Return a cached Google Cloud Pub/Sub PublisherClient instance.

    Uses publisher options for batch settings to optimize throughput.
    """
    batch_settings = pubsub_v1.types.BatchSettings(
        max_bytes=1024 * 1024,
        max_latency=0.5,
        max_messages=100,
    )
    return pubsub_v1.PublisherClient(
        batch_settings=batch_settings,
    )


@lru_cache(maxsize=2)
def get_pubsub_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Return a cached Google Cloud Pub/Sub SubscriberClient instance."""
    return pubsub_v1.SubscriberClient()


def build_topic_path(topic_id: str | None = None) -> str:
    """Build the fully qualified Google Cloud Pub/Sub topic path."""
    publisher = get_pubsub_publisher_client()
    return publisher.topic_path(PUBSUB_PROJECT_ID, topic_id or PUBSUB_TOPIC_ID)


def build_subscription_path(subscription_id: str | None = None) -> str:
    """Build the fully qualified Google Cloud Pub/Sub subscription path."""
    subscriber = get_pubsub_subscriber_client()
    return subscriber.subscription_path(
        PUBSUB_PROJECT_ID, subscription_id or PUBSUB_SUBSCRIPTION_ID
    )
