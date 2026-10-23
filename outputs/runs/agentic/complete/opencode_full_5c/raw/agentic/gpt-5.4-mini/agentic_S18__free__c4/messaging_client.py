import os
from typing import Any, Dict

from google.cloud import pubsub_v1


def project_id() -> str:
    value = (
        os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCP_PROJECT")
        or os.getenv("PUBSUB_PROJECT_ID")
    )
    if not value:
        raise RuntimeError("Missing Google Cloud project configuration")
    return value


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    return publisher_client().topic_path(project_id(), topic)


def subscription_path(subscription: str) -> str:
    return subscriber_client().subscription_path(project_id(), subscription)


def dead_letter_path(dead_letter_queue: str) -> str:
    return topic_path(dead_letter_queue)


def publish_settings() -> Dict[str, Any]:
    return {"timeout": float(os.getenv("PUBSUB_PUBLISH_TIMEOUT", "30"))}
