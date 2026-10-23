"""Local configuration and client helper utilities for Google Cloud Pub/Sub Messaging."""

import os
import json
import logging
from typing import Any, Dict, Optional
from google.cloud import pubsub_v1

logger = logging.getLogger(__name__)

# Google Cloud Pub/Sub provider configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
PUBSUB_SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
PUBSUB_DLQ_TOPIC_ID = os.environ.get("PUBSUB_DLQ_TOPIC_ID", "events-dlq-topic")

# GOOGLE_APPLICATION_CREDENTIALS is used by the Google Cloud SDK for authentication

_publisher: Optional[pubsub_v1.PublisherClient] = None
_subscriber: Optional[pubsub_v1.SubscriberClient] = None


def get_publisher() -> pubsub_v1.PublisherClient:
    """Get or create a Google Cloud Pub/Sub PublisherClient instance."""
    global _publisher
    if _publisher is None:
        _publisher = pubsub_v1.PublisherClient()
    return _publisher


def get_subscriber() -> pubsub_v1.SubscriberClient:
    """Get or create a Google Cloud Pub/Sub SubscriberClient instance."""
    global _subscriber
    if _subscriber is None:
        _subscriber = pubsub_v1.SubscriberClient()
    return _subscriber


def topic_path(topic_id: Optional[str] = None) -> str:
    """Build a fully-qualified Google Cloud Pub/Sub topic path."""
    publisher = get_publisher()
    return publisher.topic_path(PROJECT_ID, topic_id or PUBSUB_TOPIC_ID)


def subscription_path(subscription_id: Optional[str] = None) -> str:
    """Build a fully-qualified Google Cloud Pub/Sub subscription path."""
    subscriber = get_subscriber()
    return subscriber.subscription_path(PROJECT_ID, subscription_id or PUBSUB_SUBSCRIPTION_ID)


def dlq_topic_path() -> str:
    """Build a fully-qualified Google Cloud Pub/Sub DLQ topic path."""
    publisher = get_publisher()
    return publisher.topic_path(PROJECT_ID, PUBSUB_DLQ_TOPIC_ID)


def normalize_payload(payload: Any) -> bytes:
    """Serialize a payload to JSON bytes for Pub/Sub message body."""
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def decode_message_data(data: bytes) -> Dict[str, Any]:
    """Decode Pub/Sub message data bytes to a Python dict."""
    return json.loads(data.decode("utf-8"))


def build_attributes(
    event_id: Optional[str] = None,
    event_type: Optional[str] = None,
    source: Optional[str] = None,
    extra: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Build a dictionary of string attributes for a Pub/Sub message."""
    attrs: Dict[str, str] = {}
    if event_id:
        attrs["event_id"] = event_id
    if event_type:
        attrs["event_type"] = event_type
    if source:
        attrs["source"] = source
    if extra:
        attrs.update(extra)
    return attrs


def close_clients() -> None:
    """Close and reset global Pub/Sub clients for clean shutdown."""
    global _publisher, _subscriber
    if _publisher is not None:
        _publisher.close()
        _publisher = None
    if _subscriber is not None:
        _subscriber.close()
        _subscriber = None
