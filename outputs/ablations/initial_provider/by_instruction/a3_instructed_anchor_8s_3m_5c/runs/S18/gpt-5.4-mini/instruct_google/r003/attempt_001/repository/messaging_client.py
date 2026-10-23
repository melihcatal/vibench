import json
import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1


def project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    if topic.startswith("projects/"):
        return topic
    project = project_id()
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return f"projects/{project}/topics/{topic}"


def subscription_path(subscription: str) -> str:
    if subscription.startswith("projects/"):
        return subscription
    project = project_id()
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    return f"projects/{project}/subscriptions/{subscription}"


def encode_json(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def decode_json(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode("utf-8"))
