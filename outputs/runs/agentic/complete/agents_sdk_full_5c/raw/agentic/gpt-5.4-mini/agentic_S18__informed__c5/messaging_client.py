from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from google.cloud import pubsub_v1


DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
DEFAULT_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "events")
DEFAULT_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "events-sub")
DEFAULT_DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dlq")


@lru_cache(maxsize=1)
def publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


@lru_cache(maxsize=1)
def subscriber() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def project_id(explicit: Optional[str] = None) -> str:
    value = explicit or DEFAULT_PROJECT_ID
    if not value:
        raise ValueError("Missing Google Cloud project ID; set GOOGLE_CLOUD_PROJECT")
    return value


def topic_path(topic_id: str, explicit_project_id: Optional[str] = None) -> str:
    return publisher().topic_path(project_id(explicit_project_id), topic_id)


def subscription_path(subscription_id: str, explicit_project_id: Optional[str] = None) -> str:
    return subscriber().subscription_path(project_id(explicit_project_id), subscription_id)


def dead_letter_topic_path(explicit_project_id: Optional[str] = None) -> str:
    return topic_path(DEFAULT_DEAD_LETTER_TOPIC_ID, explicit_project_id)
