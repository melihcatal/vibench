import os
from functools import lru_cache
from typing import Any, Dict

from google.cloud import pubsub_v1


@lru_cache(maxsize=1)
def get_project_id() -> str:
    return os.environ.get(
        "GOOGLE_CLOUD_PROJECT", os.environ.get("GOOGLE_PROJECT_ID", "")
    )


def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def get_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    project_id = get_project_id()
    if topic.startswith("projects/"):
        return topic
    return f"projects/{project_id}/topics/{topic}"


def subscription_path(subscription: str) -> str:
    project_id = get_project_id()
    if subscription.startswith("projects/"):
        return subscription
    return f"projects/{project_id}/subscriptions/{subscription}"


def get_env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)
