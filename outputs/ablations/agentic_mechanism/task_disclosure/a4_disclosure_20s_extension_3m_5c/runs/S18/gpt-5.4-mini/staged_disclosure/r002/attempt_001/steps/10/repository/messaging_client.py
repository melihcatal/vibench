import os
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


PROJECT_ID_ENV = "GCP_PROJECT_ID"
TOPIC_ID_ENV = "PUBSUB_TOPIC_ID"
SUBSCRIPTION_ID_ENV = "PUBSUB_SUBSCRIPTION_ID"


def get_project_id() -> Optional[str]:
    return os.getenv(PROJECT_ID_ENV) or os.getenv("GOOGLE_CLOUD_PROJECT")


def get_topic_path(project_id: Optional[str] = None, topic_id: Optional[str] = None) -> str:
    project = project_id or get_project_id()
    topic = topic_id or os.getenv(TOPIC_ID_ENV)
    if not project:
        raise ValueError("Missing GCP project id")
    if not topic:
        raise ValueError("Missing Pub/Sub topic id")
    return pubsub_v1.PublisherClient().topic_path(project, topic)


def get_subscription_path(project_id: Optional[str] = None, subscription_id: Optional[str] = None) -> str:
    project = project_id or get_project_id()
    subscription = subscription_id or os.getenv(SUBSCRIPTION_ID_ENV)
    if not project:
        raise ValueError("Missing GCP project id")
    if not subscription:
        raise ValueError("Missing Pub/Sub subscription id")
    return pubsub_v1.SubscriberClient().subscription_path(project, subscription)


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def publish_message(topic_id: Optional[str], data: bytes, project_id: Optional[str] = None, **attributes: str) -> str:
    topic_path = get_topic_path(project_id=project_id, topic_id=topic_id)
    publisher = get_publisher_client()
    future = publisher.publish(topic_path, data, **attributes)
    return future.result()


def build_subscription_path(subscription_id: Optional[str] = None, project_id: Optional[str] = None) -> str:
    return get_subscription_path(project_id=project_id, subscription_id=subscription_id)
