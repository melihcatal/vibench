import os
from typing import Any, Dict

from google.cloud import pubsub_v1


def get_project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT") or ""


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    return topic if topic.startswith("projects/") else f"projects/{get_project_id()}/topics/{topic}"


def subscription_path(subscription: str) -> str:
    return subscription if subscription.startswith("projects/") else f"projects/{get_project_id()}/subscriptions/{subscription}"


def json_attributes(payload: Dict[str, Any]) -> Dict[str, str]:
    return {k: str(v) for k, v in payload.items() if v is not None}
