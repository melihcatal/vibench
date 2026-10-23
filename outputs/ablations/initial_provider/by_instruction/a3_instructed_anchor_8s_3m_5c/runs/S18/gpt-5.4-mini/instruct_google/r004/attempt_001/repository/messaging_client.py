import os
from typing import Optional

from google.cloud import pubsub_v1


def get_project_id(project_id: Optional[str] = None) -> str:
    return project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT") or os.getenv("GCLOUD_PROJECT") or ""


def get_publisher(project_id: Optional[str] = None) -> pubsub_v1.PublisherClient:
    _ = get_project_id(project_id)
    return pubsub_v1.PublisherClient()


def get_subscriber(project_id: Optional[str] = None) -> pubsub_v1.SubscriberClient:
    _ = get_project_id(project_id)
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_name: str) -> str:
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_name)


def subscription_path(project_id: str, subscription_name: str) -> str:
    return pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_name)
