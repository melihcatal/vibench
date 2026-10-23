"""Local configuration and client helper utilities for Pub/Sub Messaging.

Provides configuration loading, client initialization, and helper utilities
for Google Cloud Pub/Sub messaging integrations.
"""

import os
from typing import Optional, Dict, Any

from google.cloud import pubsub_v1
from google.api_core import retry as core_retry

# Google Cloud Pub/Sub configuration defaults
DEFAULT_PUBSUB_PROJECT_ID = os.getenv(
    "GOOGLE_CLOUD_PROJECT", "pubsub-messaging-project"
)
DEFAULT_PUBSUB_CREDENTIALS_PATH = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", ""
)

_publisher_client: Optional[pubsub_v1.PublisherClient] = None
_subscriber_client: Optional[pubsub_v1.SubscriberClient] = None


def get_pubsub_config() -> Dict[str, Any]:
    """Load Google Cloud Pub/Sub configuration from environment variables.

    Returns:
        Dictionary with project_id and credentials path.
    """
    return {
        "project_id": os.getenv(
            "PUBSUB_PROJECT_ID", DEFAULT_PUBSUB_PROJECT_ID
        ),
        "credentials_path": DEFAULT_PUBSUB_CREDENTIALS_PATH,
        "publish_timeout": float(os.getenv("PUBSUB_PUBLISH_TIMEOUT", "10.0")),
        "subscribe_timeout": float(os.getenv("PUBSUB_SUBSCRIBE_TIMEOUT", "30.0")),
        "max_delivery_attempts": int(os.getenv("PUBSUB_MAX_DELIVERY_ATTEMPTS", "5")),
        "dead_letter_topic_id": os.getenv(
            "PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
        ),
    }


def get_pubsub_publisher_client() -> pubsub_v1.PublisherClient:
    """Get or create a Google Cloud Pub/Sub publisher client.

    Returns:
        Initialized PublisherClient instance for publishing messages.
    """
    global _publisher_client
    if _publisher_client is None:
        _publisher_client = pubsub_v1.PublisherClient()
    return _publisher_client


def get_pubsub_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Get or create a Google Cloud Pub/Sub subscriber client.

    Returns:
        Initialized SubscriberClient instance for consuming messages.
    """
    global _subscriber_client
    if _subscriber_client is None:
        _subscriber_client = pubsub_v1.SubscriberClient()
    return _subscriber_client


def reset_clients() -> None:
    """Reset cached Pub/Sub clients (useful for testing)."""
    global _publisher_client, _subscriber_client
    if _publisher_client is not None:
        _publisher_client.stop()
        _publisher_client = None
    if _subscriber_client is not None:
        _subscriber_client = None


def create_retry_policy(
    initial_delay: float = 0.1,
    maximum_delay: float = 60.0,
    multiplier: float = 2.0,
    timeout: float = 600.0,
) -> core_retry.Retry:
    """Create a retry policy for Google Cloud Pub/Sub operations.

    Args:
        initial_delay: Initial delay in seconds.
        maximum_delay: Maximum delay in seconds.
        multiplier: Delay multiplier between retries.
        timeout: Total timeout in seconds.

    Returns:
        Configured Retry policy.
    """
    return core_retry.Retry(
        initial=initial_delay,
        maximum=maximum_delay,
        multiplier=multiplier,
        timeout=timeout,
    )


def build_topic_path(topic_id: str) -> str:
    """Build a full Google Cloud Pub/Sub topic path.

    Args:
        topic_id: Topic name.

    Returns:
        Full topic path string.
    """
    config = get_pubsub_config()
    publisher = get_pubsub_publisher_client()
    return publisher.topic_path(config["project_id"], topic_id)


def build_subscription_path(subscription_id: str) -> str:
    """Build a full Google Cloud Pub/Sub subscription path.

    Args:
        subscription_id: Subscription name.

    Returns:
        Full subscription path string.
    """
    config = get_pubsub_config()
    subscriber = get_pubsub_subscriber_client()
    return subscriber.subscription_path(config["project_id"], subscription_id)
