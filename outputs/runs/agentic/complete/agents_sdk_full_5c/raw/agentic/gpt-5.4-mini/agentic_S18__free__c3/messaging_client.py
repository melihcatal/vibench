import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@dataclass(frozen=True)
class MessagingConfig:
    project_id: str
    publish_topic: str
    consume_subscription: str
    dead_letter_topic: str
    audit_table: str
    location: str = "us-central1"


@lru_cache(maxsize=1)
def load_config() -> MessagingConfig:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    return MessagingConfig(
        project_id=project_id,
        publish_topic=os.environ.get("PUBSUB_TOPIC", f"projects/{project_id}/topics/events"),
        consume_subscription=os.environ.get(
            "PUBSUB_SUBSCRIPTION", f"projects/{project_id}/subscriptions/events-sub"
        ),
        dead_letter_topic=os.environ.get(
            "PUBSUB_DEAD_LETTER_TOPIC", f"projects/{project_id}/topics/events-dlq"
        ),
        audit_table=os.environ.get("AUDIT_TABLE", f"{project_id}.messaging_audit.processed_messages"),
    )


@lru_cache(maxsize=1)
def publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: Optional[str] = None) -> str:
    cfg = load_config()
    return topic or cfg.publish_topic


def subscription_path(subscription: Optional[str] = None) -> str:
    cfg = load_config()
    return subscription or cfg.consume_subscription
