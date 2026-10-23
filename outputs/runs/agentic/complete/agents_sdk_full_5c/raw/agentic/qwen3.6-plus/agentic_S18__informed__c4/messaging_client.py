"""
Local configuration and client helper utilities for Google Cloud Pub/Sub Messaging.

Provides centralized client initialization, credential handling,
and topic/subscription management helpers for the pub/sub messaging integration.
"""

import os
from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists, NotFound


GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")
GOOGLE_TOPIC_NAME = os.environ.get("PUBSUB_TOPIC_NAME", "events-topic")
GOOGLE_SUBSCRIPTION_NAME = os.environ.get("PUBSUB_SUBSCRIPTION_NAME", "events-subscription")
GOOGLE_DEAD_LETTER_TOPIC = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC", "events-dead-letter")


def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Return an initialized Google Cloud Pub/Sub publisher client."""
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Return an initialized Google Cloud Pub/Sub subscriber client."""
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str | None = None, topic_name: str | None = None) -> str:
    """Build the full Google Cloud Pub/Sub topic path string."""
    project = project_id or GOOGLE_PROJECT_ID
    name = topic_name or GOOGLE_TOPIC_NAME
    return f"projects/{project}/topics/{name}"


def subscription_path(project_id: str | None = None, subscription_name: str | None = None) -> str:
    """Build the full Google Cloud Pub/Sub subscription path string."""
    project = project_id or GOOGLE_PROJECT_ID
    name = subscription_name or GOOGLE_SUBSCRIPTION_NAME
    return f"projects/{project}/subscriptions/{name}"


def ensure_topic_exists(topic_name: str | None = None) -> str:
    """Create the Pub/Sub topic if it does not already exist. Returns the topic path."""
    client = get_publisher_client()
    path = topic_path(topic_name=topic_name)
    try:
        client.create_topic(request={"name": path})
    except AlreadyExists:
        pass
    return path


def ensure_subscription_exists(
    subscription_name: str | None = None,
    topic_name: str | None = None,
    dead_letter_topic: str | None = None,
) -> str:
    """Create the Pub/Sub subscription if it does not already exist. Optionally configure dead-letter."""
    client = get_subscriber_client()
    sub_path = subscription_path(subscription_name=subscription_name)
    top_path = topic_path(topic_name=topic_name)
    try:
        request: dict = {
            "name": sub_path,
            "topic": top_path,
        }
        if dead_letter_topic:
            dl_topic_path = topic_path(topic_name=dead_letter_topic)
            request["dead_letter_policy"] = {
                "dead_letter_topic": dl_topic_path,
                "max_delivery_attempts": 3,
            }
        client.create_subscription(request=request)
    except AlreadyExists:
        pass
    return sub_path


def publish_message_sync(
    publisher: pubsub_v1.PublisherClient,
    topic: str,
    data: bytes,
    attributes: dict | None = None,
) -> str:
    """Publish a single message synchronously and return the message ID."""
    publish_kwargs: dict = {"topic": topic, "data": data}
    if attributes:
        publish_kwargs["attributes"] = attributes
    future = publisher.publish(**publish_kwargs)
    return future.result()


def publish_batch_sync(
    publisher: pubsub_v1.PublisherClient,
    topic: str,
    messages: list[dict],
) -> list[str]:
    """Publish a batch of messages synchronously. Each message dict must contain 'data' (bytes) and optional 'attributes'. Returns list of message IDs."""
    ids: list[str] = []
    for msg in messages:
        publish_kwargs: dict = {"topic": topic, "data": msg["data"]}
        if msg.get("attributes"):
            publish_kwargs["attributes"] = msg["attributes"]
        future = publisher.publish(**publish_kwargs)
        ids.append(future.result())
    return ids
