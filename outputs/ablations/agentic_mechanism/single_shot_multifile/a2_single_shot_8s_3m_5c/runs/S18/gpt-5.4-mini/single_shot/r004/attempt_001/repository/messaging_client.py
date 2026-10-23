import os
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


@lru_cache(maxsize=1)
def get_project_id() -> str:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    return project_id


@lru_cache(maxsize=1)
def get_topic_id() -> str:
    topic_id = os.environ.get("PUBSUB_TOPIC_ID")
    if not topic_id:
        raise RuntimeError("PUBSUB_TOPIC_ID is required")
    return topic_id


@lru_cache(maxsize=1)
def get_subscription_id() -> str:
    subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID")
    if not subscription_id:
        raise RuntimeError("PUBSUB_SUBSCRIPTION_ID is required")
    return subscription_id


@lru_cache(maxsize=1)
def get_dead_letter_topic_id() -> str:
    topic_id = os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID")
    if not topic_id:
        raise RuntimeError("PUBSUB_DEAD_LETTER_TOPIC_ID is required")
    return topic_id


@lru_cache(maxsize=1)
def get_publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def get_publish_topic_path() -> str:
    return get_publisher_client().topic_path(get_project_id(), get_topic_id())


def get_subscription_path() -> str:
    return get_subscriber_client().subscription_path(get_project_id(), get_subscription_id())


def get_dead_letter_topic_path() -> str:
    return get_publisher_client().topic_path(get_project_id(), get_dead_letter_topic_id())
