import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import pubsub_v1


@dataclass
class MessagingSettings:
    project_id: str
    topic_id: str
    subscription_id: str
    dead_letter_topic_id: str


def load_settings() -> MessagingSettings:
    return MessagingSettings(
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT", os.environ.get("GCP_PROJECT", "")),
        topic_id=os.environ.get("PUBSUB_TOPIC_ID", "events-topic"),
        subscription_id=os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription"),
        dead_letter_topic_id=os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter"),
    )


def get_project_id(settings: Optional[MessagingSettings] = None) -> str:
    settings = settings or load_settings()
    if not settings.project_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT or GCP_PROJECT")
    return settings.project_id


def get_topic_path(project_id: str, topic_id: str) -> str:
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_id)


def get_subscription_path(project_id: str, subscription_id: str) -> str:
    return pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)
