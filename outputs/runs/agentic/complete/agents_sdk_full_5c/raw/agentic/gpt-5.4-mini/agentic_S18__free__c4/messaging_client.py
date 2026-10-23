import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str
    audit_topic_id: str
    location: str = "us-central1"


@lru_cache(maxsize=1)
def load_config() -> MessagingConfig:
    project_id = os.environ.get("GCP_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT is required")
    return MessagingConfig(
        project_id=project_id,
        topic_id=os.environ.get("PUBSUB_TOPIC_ID", "events"),
        subscription_id=os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-sub"),
        dead_letter_topic_id=os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dlq"),
        audit_topic_id=os.environ.get("PUBSUB_AUDIT_TOPIC_ID", "events-audit"),
        location=os.environ.get("PUBSUB_LOCATION", "us-central1"),
    )


@lru_cache(maxsize=1)
def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: str, project_id: Optional[str] = None) -> str:
    cfg = load_config()
    return publisher_client().topic_path(project_id or cfg.project_id, topic_id)


def subscription_path(subscription_id: str, project_id: Optional[str] = None) -> str:
    cfg = load_config()
    return subscriber_client().subscription_path(project_id or cfg.project_id, subscription_id)
