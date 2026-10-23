"""Local configuration and client helper utilities for Google Cloud Pub/Sub Messaging."""

import os
from google.cloud.pubsub_v1 import PublisherClient, SubscriberClient
from google.cloud.pubsub_v1.types import BatchSettings, PublishBatchSettings


DEFAULT_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "my-gcp-project")
DEFAULT_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events-topic")
DEFAULT_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
DEFAULT_DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter")
DEFAULT_MAX_RETRIES = int(os.getenv("PUBSUB_MAX_RETRIES", "3"))


def get_publisher_client(batch_size: int = 10, max_latency: float = 1.0) -> PublisherClient:
    """Create and return a configured Google Cloud Pub/Sub PublisherClient.

    Args:
        batch_size: Maximum number of messages per batch publish.
        max_latency: Maximum latency in seconds before publishing a batch.

    Returns:
        Configured PublisherClient instance.
    """
    batch_settings = PublishBatchSettings(
        max_messages=batch_size,
        max_latency=max_latency,
    )
    return PublisherClient(default_publish_settings=batch_settings)


def get_subscriber_client() -> SubscriberClient:
    """Create and return a Google Cloud Pub/Sub SubscriberClient.

    Returns:
        Configured SubscriberClient instance.
    """
    return SubscriberClient()


def topic_path(project_id: str | None = None, topic_id: str | None = None) -> str:
    """Build a fully-qualified Pub/Sub topic path.

    Args:
        project_id: GCP project ID. Defaults to DEFAULT_PROJECT_ID.
        topic_id: Topic identifier. Defaults to DEFAULT_TOPIC_ID.

    Returns:
        Fully-qualified topic path string.
    """
    pid = project_id or DEFAULT_PROJECT_ID
    tid = topic_id or DEFAULT_TOPIC_ID
    return f"projects/{pid}/topics/{tid}"


def subscription_path(
    project_id: str | None = None,
    subscription_id: str | None = None,
) -> str:
    """Build a fully-qualified Pub/Sub subscription path.

    Args:
        project_id: GCP project ID. Defaults to DEFAULT_PROJECT_ID.
        subscription_id: Subscription identifier. Defaults to DEFAULT_SUBSCRIPTION_ID.

    Returns:
        Fully-qualified subscription path string.
    """
    pid = project_id or DEFAULT_PROJECT_ID
    sid = subscription_id or DEFAULT_SUBSCRIPTION_ID
    return f"projects/{pid}/subscriptions/{sid}"


def dead_letter_topic_path(
    project_id: str | None = None,
    topic_id: str | None = None,
) -> str:
    """Build a fully-qualified Pub/Sub dead-letter topic path.

    Args:
        project_id: GCP project ID. Defaults to DEFAULT_PROJECT_ID.
        topic_id: Dead-letter topic identifier. Defaults to DEFAULT_DEAD_LETTER_TOPIC_ID.

    Returns:
        Fully-qualified dead-letter topic path string.
    """
    pid = project_id or DEFAULT_PROJECT_ID
    tid = topic_id or DEFAULT_DEAD_LETTER_TOPIC_ID
    return f"projects/{pid}/topics/{tid}"


def get_max_retries() -> int:
    """Return the configured maximum retry count for message processing.

    Returns:
        Maximum number of retries before sending to dead-letter queue.
    """
    return DEFAULT_MAX_RETRIES
