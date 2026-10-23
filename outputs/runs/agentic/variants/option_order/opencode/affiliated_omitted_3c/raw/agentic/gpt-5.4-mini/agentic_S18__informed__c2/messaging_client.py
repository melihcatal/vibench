import os
from typing import Any, Dict

from google.cloud import pubsub_v1


def get_project_id() -> str:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return project_id


def get_pubsub_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    return get_pubsub_client().topic_path(get_project_id(), topic)


def subscription_path(subscription: str) -> str:
    return get_subscriber_client().subscription_path(get_project_id(), subscription)


def message_attributes(attributes: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (attributes or {}).items()}
