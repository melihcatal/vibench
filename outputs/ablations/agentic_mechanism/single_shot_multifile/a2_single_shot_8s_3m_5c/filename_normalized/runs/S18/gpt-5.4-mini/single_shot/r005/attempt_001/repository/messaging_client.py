import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingSettings:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str
    timeout_seconds: int = 10


@lru_cache(maxsize=1)
def load_settings() -> MessagingSettings:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT") or ""
    topic_id = os.environ.get("PUBSUB_TOPIC_ID") or "events"
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID") or "events-sub"
    dead_letter_topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID") or "events-dlq"
    timeout_seconds = int(os.environ.get("PUBSUB_TIMEOUT_SECONDS", "10"))
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or GCP_PROJECT is required")
    return MessagingSettings(project_id, topic_id, subscription_id, dead_letter_topic_id, timeout_seconds)


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def get_topic_path(client: pubsub_v1.PublisherClient, project_id: str, topic_id: str) -> str:
    return client.topic_path(project_id, topic_id)


def get_subscription_path(client: pubsub_v1.SubscriberClient, project_id: str, subscription_id: str) -> str:
    return client.subscription_path(project_id, subscription_id)
