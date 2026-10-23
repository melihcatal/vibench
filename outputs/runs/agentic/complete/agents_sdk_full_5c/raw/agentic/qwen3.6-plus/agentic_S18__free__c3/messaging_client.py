"""Provide local configuration and client helper utilities for Pub/Sub Messaging.

Uses Google Cloud Pub/Sub as the managed messaging provider.
"""

import os
import json
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


# Google Cloud Pub/Sub configuration
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
PUBSUB_TOPIC_NAME = os.environ.get("PUBSUB_TOPIC_NAME", "events-topic")
PUBSUB_SUBSCRIPTION_NAME = os.environ.get("PUBSUB_SUBSCRIPTION_NAME", "events-subscription")
PUBSUB_DEAD_LETTER_TOPIC = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "dead-letter-topic")
PUBSUB_DEAD_LETTER_SUBSCRIPTION = os.environ.get("PUBSUB_DEAD_LETTER_SUBSCRIPTION", "dead-letter-subscription")


def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Create and return a Google Cloud Pub/Sub publisher client."""
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Create and return a Google Cloud Pub/Sub subscriber client."""
    return pubsub_v1.SubscriberClient()


def get_topic_path(project: Optional[str] = None, topic_name: Optional[str] = None) -> str:
    """Get the fully-qualified topic path for Google Cloud Pub/Sub."""
    proj = project or GOOGLE_CLOUD_PROJECT
    topic = topic_name or PUBSUB_TOPIC_NAME
    return f"projects/{proj}/topics/{topic}"


def get_subscription_path(project: Optional[str] = None, subscription_name: Optional[str] = None) -> str:
    """Get the fully-qualified subscription path for Google Cloud Pub/Sub."""
    proj = project or GOOGLE_CLOUD_PROJECT
    sub = subscription_name or PUBSUB_SUBSCRIPTION_NAME
    return f"projects/{proj}/subscriptions/{sub}"


def get_dead_letter_topic_path(project: Optional[str] = None, topic_name: Optional[str] = None) -> str:
    """Get the fully-qualified dead-letter topic path."""
    proj = project or GOOGLE_CLOUD_PROJECT
    topic = topic_name or PUBSUB_DEAD_LETTER_TOPIC
    return f"projects/{proj}/topics/{topic}"


def encode_message(data: Dict[str, Any]) -> bytes:
    """Encode a message dictionary to bytes for Google Cloud Pub/Sub."""
    return json.dumps(data).encode("utf-8")


def decode_message(message_data: bytes) -> Dict[str, Any]:
    """Decode message bytes from Google Cloud Pub/Sub to a dictionary."""
    return json.loads(message_data.decode("utf-8"))


def build_attributes(attributes: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Build or return message attributes for Google Cloud Pub/Sub."""
    if attributes is None:
        return {}
    return {k: str(v) for k, v in attributes.items()}
