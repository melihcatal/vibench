import os
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


PROJECT_ID_ENV = "GCP_PROJECT_ID"
TOPIC_ID_ENV = "GCP_PUBSUB_TOPIC"
SUBSCRIPTION_ID_ENV = "GCP_PUBSUB_SUBSCRIPTION"
DLQ_TOPIC_ID_ENV = "GCP_PUBSUB_DLQ_TOPIC"


@lru_cache(maxsize=1)
def get_project_id(explicit: Optional[str] = None) -> str:
    project_id = explicit or os.getenv(PROJECT_ID_ENV) or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Missing Google Cloud project id")
    return project_id


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_id: str) -> str:
    return get_publisher_client().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return get_subscriber_client().subscription_path(project_id, subscription_id)


def resolve_topic_id(explicit: Optional[str] = None) -> str:
    topic_id = explicit or os.getenv(TOPIC_ID_ENV)
    if not topic_id:
        raise ValueError("Missing Pub/Sub topic id")
    return topic_id


def resolve_subscription_id(explicit: Optional[str] = None) -> str:
    subscription_id = explicit or os.getenv(SUBSCRIPTION_ID_ENV)
    if not subscription_id:
        raise ValueError("Missing Pub/Sub subscription id")
    return subscription_id


def resolve_dlq_topic_id(explicit: Optional[str] = None) -> str:
    dlq_topic_id = explicit or os.getenv(DLQ_TOPIC_ID_ENV)
    if not dlq_topic_id:
        raise ValueError("Missing Pub/Sub dead-letter topic id")
    return dlq_topic_id
