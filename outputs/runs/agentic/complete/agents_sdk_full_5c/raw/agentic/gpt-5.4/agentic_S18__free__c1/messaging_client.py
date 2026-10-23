from __future__ import annotations

import os
from typing import Iterable

from google.cloud import pubsub_v1

from messaging_models import PubSubEvent


PUBSUB_PROJECT_ID = os.getenv("GCP_PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
PUBSUB_TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "customer-events")
PUBSUB_SUBSCRIPTION_ID = os.getenv("PUBSUB_SUBSCRIPTION_ID", "customer-events-sub")
PUBSUB_DEAD_LETTER_TOPIC_ID = os.getenv("PUBSUB_DEAD_LETTER_TOPIC_ID", "customer-events-dlq")


class PubSubConfigError(ValueError):
    pass


def require_project_id() -> str:
    if not PUBSUB_PROJECT_ID:
        raise PubSubConfigError("Set GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT for Google Cloud Pub/Sub.")
    return PUBSUB_PROJECT_ID


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: str | None = None) -> str:
    client = publisher_client()
    return client.topic_path(require_project_id(), topic_id or PUBSUB_TOPIC_ID)


def subscription_path(subscription_id: str | None = None) -> str:
    client = subscriber_client()
    return client.subscription_path(require_project_id(), subscription_id or PUBSUB_SUBSCRIPTION_ID)


def dead_letter_topic_path() -> str:
    return topic_path(PUBSUB_DEAD_LETTER_TOPIC_ID)


def build_publish_kwargs(event: PubSubEvent) -> dict:
    kwargs = dict(event.attributes.values)
    if event.ordering_key:
        kwargs["ordering_key"] = event.ordering_key
    return kwargs


def build_batch_payloads(events: Iterable[PubSubEvent]) -> list[tuple[bytes, dict]]:
    payloads: list[tuple[bytes, dict]] = []
    for event in events:
        payloads.append((event.to_json_bytes(), build_publish_kwargs(event)))
    return payloads
