import os
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@lru_cache(maxsize=1)
def build_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def build_subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def resolve_project_id(explicit: Optional[str] = None) -> str:
    project_id = explicit or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project id is required")
    return project_id


def resolve_topic_path(project_id: Optional[str], topic_id: str) -> str:
    return build_publisher().topic_path(resolve_project_id(project_id), topic_id)


def resolve_subscription_path(project_id: Optional[str], subscription_id: str) -> str:
    return build_subscriber().subscription_path(resolve_project_id(project_id), subscription_id)
