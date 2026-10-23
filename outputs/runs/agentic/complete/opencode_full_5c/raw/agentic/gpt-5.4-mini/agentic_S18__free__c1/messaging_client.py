import os
from typing import Any, Dict

from google.cloud import pubsub_v1


def project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", ""))


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    return f"projects/{project_id()}/topics/{topic}"


def subscription_path(subscription: str) -> str:
    return f"projects/{project_id()}/subscriptions/{subscription}"


def encode_json(data: Dict[str, Any]) -> bytes:
    import json

    return json.dumps(data, separators=(",", ":")).encode("utf-8")
