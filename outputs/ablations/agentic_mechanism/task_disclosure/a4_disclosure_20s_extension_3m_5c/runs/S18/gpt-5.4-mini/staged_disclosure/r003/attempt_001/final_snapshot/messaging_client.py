import os
from dataclasses import dataclass
from typing import Dict, Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class PubSubConfig:
    project_id: str
    topic_id: Optional[str] = None
    subscription_id: Optional[str] = None


def load_pubsub_config() -> PubSubConfig:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return PubSubConfig(
        project_id=project_id,
        topic_id=os.environ.get("PUBSUB_TOPIC_ID"),
        subscription_id=os.environ.get("PUBSUB_SUBSCRIPTION"),
    )


def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_id: str) -> str:
    return get_publisher_client().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return get_subscriber_client().subscription_path(project_id, subscription_id)


def default_topic_path() -> str:
    config = load_pubsub_config()
    if not config.topic_id:
        raise RuntimeError("PUBSUB_TOPIC_ID is required")
    return topic_path(config.project_id, config.topic_id)


def default_subscription_path() -> str:
    config = load_pubsub_config()
    if not config.subscription_id:
        raise RuntimeError("PUBSUB_SUBSCRIPTION is required")
    return subscription_path(config.project_id, config.subscription_id)


def publish_json(publisher: pubsub_v1.PublisherClient, topic: str, data: Dict[str, object], attributes: Optional[Dict[str, str]] = None) -> str:
    payload = str(data).encode("utf-8")
    future = publisher.publish(topic, payload, content_type="application/json", **(attributes or {}))
    return future.result()
